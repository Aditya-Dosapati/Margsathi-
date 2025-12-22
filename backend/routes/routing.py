from math import radians, cos, sin, asin, sqrt
from typing import List, Literal, Optional, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter()


TravelMode = Literal["car", "bike", "walk", "transit"]


class Coordinate(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class RouteLeg(BaseModel):
    start: Coordinate
    end: Coordinate
    distance_meters: float
    duration_seconds: float
    mode: TravelMode


class RouteSummary(BaseModel):
    distance_meters: float
    duration_seconds: float
    estimated_co2_kg: float


class RouteRequest(BaseModel):
    origin: Coordinate
    destination: Coordinate
    mode: TravelMode = "car"
    departure_time: Optional[str] = Field(
        default=None,
        description="ISO8601 timestamp, optional. Used for future real-time integrations.",
    )


class RouteResponse(BaseModel):
    waypoints: List[Coordinate]
    legs: List[RouteLeg]
    summary: RouteSummary
    debug: dict = Field(
        default_factory=dict,
        description="Extra hackathon-friendly debug info.",
    )


class AlternateRouteRequest(RouteRequest):
    event_type: str = Field(
        ...,
        description=(
            "Type of mobility event to consider when suggesting alternates, "
            "e.g. 'road_closure', 'protest', 'concert'."
        ),
    )


class AlternateRouteResponse(BaseModel):
    base_route: RouteResponse
    alternate_route: RouteResponse
    reasoning: str = Field(
        ...,
        description="Human-readable explanation of how events influenced the suggestion.",
    )


def _haversine_distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Simple haversine implementation to approximate distance in meters.

    This keeps the demo self-contained without needing external routing APIs.
    """
    r = 6371000  # Earth radius in meters

    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    )
    c = 2 * asin(sqrt(a))
    return r * c


def _estimate_speed_mps(mode: TravelMode) -> float:
    if mode == "walk":
        return 1.4  # ~5 km/h
    if mode == "bike":
        return 4.1  # ~15 km/h
    if mode == "transit":
        return 8.3  # ~30 km/h (averaged)
    return 13.9  # car ~50 km/h urban average


def _estimate_co2_kg(distance_m: float, mode: TravelMode) -> float:
    # Very rough, illustrative values only (kg per km)
    if mode == "walk" or mode == "bike":
        return 0.0
    if mode == "transit":
        factor = 0.08
    else:  # car
        factor = 0.18
    return round((distance_m / 1000.0) * factor, 3)


@router.post("/plan", response_model=RouteResponse, summary="Plan a simple route")
async def plan_route(payload: RouteRequest) -> RouteResponse:
    """
    Plan a simple, single-leg route between two coordinates.

    This is intentionally lightweight and self-contained so that it
    works offline during hackathons and demos. In a real deployment
    you would swap this out for a proper routing engine or external API.
    """
    distance_m = _haversine_distance_m(
        payload.origin.lat,
        payload.origin.lon,
        payload.destination.lat,
        payload.destination.lon,
    )

    speed_mps = _estimate_speed_mps(payload.mode)
    duration_s = distance_m / speed_mps if speed_mps > 0 else 0

    leg = RouteLeg(
        start=payload.origin,
        end=payload.destination,
        distance_meters=round(distance_m, 2),
        duration_seconds=round(duration_s, 1),
        mode=payload.mode,
    )

    summary = RouteSummary(
        distance_meters=leg.distance_meters,
        duration_seconds=leg.duration_seconds,
        estimated_co2_kg=_estimate_co2_kg(distance_m, payload.mode),
    )

    return RouteResponse(
        waypoints=[payload.origin, payload.destination],
        legs=[leg],
        summary=summary,
        debug={
            "implementation": "haversine_stub",
            "note": "Replace with real routing in production.",
        },
    )


@router.post(
    "/plan/alternate",
    response_model=AlternateRouteResponse,
    summary="Suggest an alternate route based on event type (mocked)",
)
async def plan_alternate_route(
    payload: AlternateRouteRequest,
) -> AlternateRouteResponse:
    """
    Suggest an alternate route based on the type of mobility event.

    Since we don't call real map APIs here, we use simple, transparent
    mock logic:

    - First compute the base route exactly like `/plan`.
    - Then adjust distance and duration by a multiplier that depends
      on `event_type` to simulate detours or slower traffic.
    - We keep the same origin/destination waypoints but clearly explain
      the assumptions in the `reasoning` field.
    """
    base = await plan_route(payload)  # reuse existing logic

    # Mock impact factors by event type
    normalized = payload.event_type.lower().strip()
    if normalized in {"road_closure", "accident", "construction"}:
        factor = 1.3  # 30% longer detour
        reason = (
            "Road closures typically force a detour around the blocked segment, "
            "so we assume about 30% extra distance and time."
        )
    elif normalized in {"protest", "rally", "parade"}:
        factor = 1.2  # slower traffic, mild detour
        reason = (
            "Protests and rallies can slow traffic and partially block streets, "
            "so we assume around 20% extra distance and time."
        )
    elif normalized in {"concert", "sports", "event"}:
        factor = 1.15  # congestion near venue
        reason = (
            "Large events create localized congestion near the venue, so we "
            "assume a 15% increase in distance and travel time for a smarter route."
        )
    else:
        factor = 1.05  # small generic buffer
        reason = (
            "Unknown event type. We apply a small 5% buffer as a conservative "
            "detour estimate while keeping the route close to the base plan."
        )

    alt_distance = round(base.summary.distance_meters * factor, 2)
    alt_duration = round(base.summary.duration_seconds * factor, 1)

    alt_summary = RouteSummary(
        distance_meters=alt_distance,
        duration_seconds=alt_duration,
        estimated_co2_kg=_estimate_co2_kg(alt_distance, payload.mode),
    )

    alt_leg = RouteLeg(
        start=payload.origin,
        end=payload.destination,
        distance_meters=alt_distance,
        duration_seconds=alt_duration,
        mode=payload.mode,
    )

    alternate = RouteResponse(
        waypoints=base.waypoints,
        legs=[alt_leg],
        summary=alt_summary,
        debug={
            "implementation": "event_type_multiplier_stub",
            "event_type": payload.event_type,
            "multiplier": factor,
        },
    )

    return AlternateRouteResponse(
        base_route=base,
        alternate_route=alternate,
        reasoning=reason,
    )


# ============================================================================
# Text-based location routing endpoint
# ============================================================================

class TextRouteRequest(BaseModel):
    source: str = Field(..., description="Starting location name (e.g., 'BTM Layout')")
    destination: str = Field(..., description="Destination location name (e.g., 'MG Road')")
    event: str = Field(
        default="",
        description="Event affecting the route (e.g., 'Political Rally', 'Road Closure')",
    )
    mode: TravelMode = Field(default="car", description="Travel mode: car, bike, walk, or transit")


class TextRouteResponse(BaseModel):
    recommended_route: str = Field(
        ...,
        description="Human-readable route description with waypoints",
    )
    reason: str = Field(
        ...,
        description="Explanation of why this route was recommended",
    )
    distance_meters: float = Field(..., description="Total distance in meters")
    distance_km: float = Field(..., description="Total distance in kilometers")
    duration_seconds: float = Field(..., description="Estimated travel time in seconds")
    duration_minutes: float = Field(..., description="Estimated travel time in minutes")
    estimated_co2_kg: float = Field(..., description="Estimated CO2 emissions in kg")
    waypoints: List[str] = Field(
        ...,
        description="List of waypoint names in order",
    )


# Mock geocoding database for Bangalore locations
# In production, replace this with a real geocoding service (Google Maps, OSM Nominatim, etc.)
LOCATION_DB: Dict[str, Dict[str, float]] = {
    "btm layout": {"lat": 12.9166, "lon": 77.6101, "display": "BTM Layout"},
    "mg road": {"lat": 12.9716, "lon": 77.5946, "display": "MG Road"},
    "jp nagar": {"lat": 12.9067, "lon": 77.5858, "display": "JP Nagar"},
    "richmond road": {"lat": 12.9500, "lon": 77.6000, "display": "Richmond Road"},
    "lalbagh": {"lat": 12.9507, "lon": 77.5848, "display": "Lalbagh"},
    "indiranagar": {"lat": 12.9784, "lon": 77.6408, "display": "Indiranagar"},
    "koramangala": {"lat": 12.9352, "lon": 77.6245, "display": "Koramangala"},
    "whitefield": {"lat": 12.9698, "lon": 77.7499, "display": "Whitefield"},
    "marathahalli": {"lat": 12.9592, "lon": 77.6974, "display": "Marathahalli"},
    "hebbal": {"lat": 13.0358, "lon": 77.5970, "display": "Hebbal"},
    "electronic city": {"lat": 12.8456, "lon": 77.6633, "display": "Electronic City"},
    "cubbon park": {"lat": 12.9716, "lon": 77.5946, "display": "Cubbon Park"},
    "ulsoor": {"lat": 12.9784, "lon": 77.6408, "display": "Ulsoor"},
    "malleshwaram": {"lat": 13.0050, "lon": 77.5610, "display": "Malleshwaram"},
    "rajajinagar": {"lat": 12.9784, "lon": 77.5510, "display": "Rajajinagar"},
}


def _geocode_location(location_name: str) -> Dict[str, float]:
    """
    Mock geocoding function that looks up location names.
    
    In production, replace this with a real geocoding API call.
    """
    normalized = location_name.lower().strip()
    
    # Direct match
    if normalized in LOCATION_DB:
        return LOCATION_DB[normalized]
    
    # Partial match (e.g., "BTM" matches "BTM Layout")
    for key, value in LOCATION_DB.items():
        if normalized in key or key in normalized:
            return value
    
    # Default fallback: use a central Bangalore coordinate
    # In production, you'd raise an error or call a real geocoding service
    return {"lat": 12.9716, "lon": 77.5946, "display": location_name.title()}


def _generate_waypoints(
    source: str, destination: str, event: str
) -> tuple[List[str], str]:
    """
    Generate realistic waypoints based on source, destination, and event.
    
    This is mock logic that creates believable route descriptions.
    In production, use a real routing engine (Google Directions, OSRM, etc.).
    """
    source_norm = source.lower().strip()
    dest_norm = destination.lower().strip()
    event_norm = event.lower().strip()
    
    waypoints = [source]
    
    # Generate route based on known location combinations
    if "btm" in source_norm and "mg road" in dest_norm:
        if "rally" in event_norm or "protest" in event_norm or "lalbagh" in event_norm:
            # Avoid Lalbagh area due to rally
            waypoints.extend(["JP Nagar", "Richmond Road"])
            reason = "Avoiding rally congestion near Lalbagh"
        else:
            waypoints.extend(["JP Nagar", "Richmond Road"])
            reason = "Optimal route via JP Nagar and Richmond Road"
    
    elif "btm" in source_norm and "koramangala" in dest_norm:
        waypoints.extend(["HSR Layout"])
        reason = "Direct route via HSR Layout"
    
    elif "indiranagar" in source_norm and "mg road" in dest_norm:
        waypoints.extend(["Ulsoor"])
        reason = "Route via Ulsoor"
    
    elif "whitefield" in source_norm and "mg road" in dest_norm:
        waypoints.extend(["Marathahalli", "Indiranagar"])
        if "event" in event_norm or "traffic" in event_norm:
            reason = "Avoiding heavy traffic on main corridor"
        else:
            reason = "Standard route via Marathahalli and Indiranagar"
    
    elif "electronic city" in source_norm and "mg road" in dest_norm:
        waypoints.extend(["BTM Layout", "Richmond Road"])
        reason = "Route via BTM Layout and Richmond Road"
    
    else:
        # Generic route generation
        if event_norm:
            waypoints.append("via alternate route")
            reason = f"Avoiding {event} by taking alternate route"
        else:
            waypoints.append("via main road")
            reason = "Standard route recommendation"
    
    waypoints.append(destination)
    
    # Format route string
    route_str = " → ".join(waypoints)
    
    return waypoints, reason


@router.post(
    "/suggest",
    response_model=TextRouteResponse,
    summary="Get route suggestion using text-based locations",
)
async def suggest_text_route(payload: TextRouteRequest) -> TextRouteResponse:
    """
    Suggest a route between two text-based locations (e.g., "BTM Layout" to "MG Road").
    
    This endpoint:
    - Accepts location names as strings (not coordinates)
    - Considers events that might affect routing
    - Returns a human-readable route description with waypoints
    - Includes distance, duration, and CO2 estimates
    
    Example request:
    ```json
    {
      "source": "BTM Layout",
      "destination": "MG Road",
      "event": "Political Rally"
    }
    ```
    
    Example response:
    ```json
    {
      "recommended_route": "BTM Layout → JP Nagar → Richmond Road → MG Road",
      "reason": "Avoiding rally congestion near Lalbagh",
      "distance_meters": 6500.0,
      "distance_km": 6.5,
      "duration_seconds": 468.0,
      "duration_minutes": 7.8,
      "estimated_co2_kg": 1.17,
      "waypoints": ["BTM Layout", "JP Nagar", "Richmond Road", "MG Road"]
    }
    ```
    """
    # Geocode source and destination
    source_coords = _geocode_location(payload.source)
    dest_coords = _geocode_location(payload.destination)
    
    # Generate waypoints and reasoning
    waypoints, reason = _generate_waypoints(
        source_coords.get("display", payload.source),
        dest_coords.get("display", payload.destination),
        payload.event,
    )
    
    # Calculate distance using haversine
    distance_m = _haversine_distance_m(
        source_coords["lat"],
        source_coords["lon"],
        dest_coords["lat"],
        dest_coords["lon"],
    )
    
    # Apply event-based multiplier if event is specified
    if payload.event:
        event_norm = payload.event.lower().strip()
        if any(x in event_norm for x in ["rally", "protest", "parade", "political"]):
            distance_m *= 1.2  # 20% longer due to detour
            reason = f"Avoiding {payload.event.lower()} congestion"
        elif any(x in event_norm for x in ["closure", "accident", "construction"]):
            distance_m *= 1.3  # 30% longer due to detour
            reason = f"Detouring around {payload.event.lower()}"
        elif any(x in event_norm for x in ["concert", "sports", "event"]):
            distance_m *= 1.15  # 15% longer due to congestion
            reason = f"Avoiding {payload.event.lower()} traffic"
    
    # Calculate duration
    speed_mps = _estimate_speed_mps(payload.mode)
    duration_s = distance_m / speed_mps if speed_mps > 0 else 0
    
    # Calculate CO2
    co2_kg = _estimate_co2_kg(distance_m, payload.mode)
    
    # Format route string
    route_str = " → ".join(waypoints)
    
    return TextRouteResponse(
        recommended_route=route_str,
        reason=reason,
        distance_meters=round(distance_m, 2),
        distance_km=round(distance_m / 1000.0, 2),
        duration_seconds=round(duration_s, 1),
        duration_minutes=round(duration_s / 60.0, 1),
        estimated_co2_kg=co2_kg,
        waypoints=waypoints,
    )

