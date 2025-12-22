from datetime import datetime, time
from typing import List, Optional, Literal
from enum import Enum

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field


router = APIRouter()


class ParkingLocation(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    capacity: int = Field(..., ge=0)
    occupied: int = Field(..., ge=0)
    pricing_per_hour: float = Field(..., ge=0)
    source: str = Field(
        default="mock",
        description="Data source identifier (e.g. 'mock', 'city-open-data').",
    )

    @property
    def available(self) -> int:
        return max(self.capacity - self.occupied, 0)


class ParkingSearchResponse(BaseModel):
    items: List[ParkingLocation]
    count: int
    center_lat: float
    center_lon: float
    radius_m: int


MOCK_PARKING_SPOTS: List[ParkingLocation] = [
    ParkingLocation(
        id="p1",
        name="MARGSATHI Central Hub Parking",
        lat=12.9716,
        lon=77.5946,
        capacity=150,
        occupied=96,
        pricing_per_hour=30.0,
    ),
    ParkingLocation(
        id="p2",
        name="Metro Station Park & Ride",
        lat=12.9796,
        lon=77.5996,
        capacity=300,
        occupied=210,
        pricing_per_hour=20.0,
    ),
    ParkingLocation(
        id="p3",
        name="Tech Park Visitor Parking",
        lat=12.9352,
        lon=77.6245,
        capacity=80,
        occupied=52,
        pricing_per_hour=40.0,
    ),
]


@router.get(
    "/search",
    response_model=ParkingSearchResponse,
    summary="Search for nearby parking",
)
async def search_parking(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_m: int = Query(
        1000,
        ge=100,
        le=10000,
        description="Search radius in meters. Defaults to 1000m.",
    ),
    max_results: Optional[int] = Query(
        10,
        ge=1,
        le=50,
        description="Maximum number of parking locations to return.",
    ),
) -> ParkingSearchResponse:
    """
    Lightweight, hackathon-ready parking search.

    For now this returns a filtered subset of in-memory mock data. You can
    later replace `MOCK_PARKING_SPOTS` with a database query or live feed.
    """
    # In a real implementation you'd do geo-filtering. For now, we just
    # pretend the mock points are "nearby" and slice to the requested size.
    items = MOCK_PARKING_SPOTS[:max_results]

    return ParkingSearchResponse(
        items=items,
        count=len(items),
        center_lat=lat,
        center_lon=lon,
        radius_m=radius_m,
    )


# ============================================================================
# Parking Availability Predictor
# ============================================================================

class AvailabilityLevel(str, Enum):
    """Parking availability levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class AreaType(str, Enum):
    """Area type classification"""
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    MIXED = "mixed"


class ParkingPredictRequest(BaseModel):
    area: str = Field(..., description="Area name (e.g., 'MG Road', 'BTM Layout')")
    area_type: AreaType = Field(
        default=AreaType.COMMERCIAL,
        description="Type of area: commercial, residential, or mixed",
    )
    time_of_day: Optional[str] = Field(
        default=None,
        description="Time in HH:MM format (24-hour). If not provided, uses current time.",
    )


class ParkingPredictResponse(BaseModel):
    area: str
    availability: AvailabilityLevel
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0 to 1.0)")
    predicted_occupancy_percent: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Predicted occupancy percentage",
    )
    time_of_day: str
    area_type: AreaType
    factors: dict = Field(
        ...,
        description="Factors influencing the prediction (for transparency)",
    )


# Mock historical occupancy data by area and hour
# In production, this would come from a time-series database or ML model
MOCK_HISTORICAL_OCCUPANCY: dict = {
    "MG Road": {
        "commercial": {
            # Hour -> average occupancy percentage
            8: 45,   # Morning rush
            9: 75,   # Peak morning
            10: 85,  # Peak
            11: 90,  # Peak
            12: 95,  # Lunch peak
            13: 88,  # Post-lunch
            14: 85,  # Afternoon
            15: 80,  # Afternoon
            16: 75,  # Evening start
            17: 70,  # Evening
            18: 60,  # Evening
            19: 50,  # Evening end
            20: 35,  # Night
            21: 25,  # Late night
            22: 15,  # Late night
        },
        "residential": {
            8: 20, 9: 15, 10: 10, 11: 8, 12: 5, 13: 5, 14: 8, 15: 10, 16: 15,
            17: 25, 18: 40, 19: 55, 20: 60, 21: 55, 22: 45,
        },
        "mixed": {
            8: 35, 9: 50, 10: 60, 11: 70, 12: 80, 13: 75, 14: 70, 15: 65, 16: 60,
            17: 55, 18: 50, 19: 45, 20: 35, 21: 25, 22: 20,
        },
    },
    "BTM Layout": {
        "commercial": {
            8: 40, 9: 70, 10: 80, 11: 85, 12: 90, 13: 85, 14: 80, 15: 75, 16: 70,
            17: 65, 18: 55, 19: 45, 20: 30, 21: 20, 22: 15,
        },
        "residential": {
            8: 25, 9: 20, 10: 15, 11: 12, 12: 10, 13: 10, 14: 12, 15: 15, 16: 20,
            17: 30, 18: 45, 19: 60, 20: 65, 21: 60, 22: 50,
        },
        "mixed": {
            8: 30, 9: 45, 10: 55, 11: 65, 12: 75, 13: 70, 14: 65, 15: 60, 16: 55,
            17: 50, 18: 45, 19: 40, 20: 30, 21: 25, 22: 20,
        },
    },
    # Default pattern for unknown areas
    "default": {
        "commercial": {
            8: 50, 9: 75, 10: 85, 11: 90, 12: 92, 13: 88, 14: 85, 15: 80, 16: 75,
            17: 70, 18: 60, 19: 50, 20: 40, 21: 30, 22: 25,
        },
        "residential": {
            8: 30, 9: 25, 10: 20, 11: 15, 12: 12, 13: 12, 14: 15, 15: 20, 16: 25,
            17: 35, 18: 50, 19: 60, 20: 65, 21: 60, 22: 50,
        },
        "mixed": {
            8: 40, 9: 55, 10: 65, 11: 75, 12: 80, 13: 75, 14: 70, 15: 65, 16: 60,
            17: 55, 18: 50, 19: 45, 20: 35, 21: 30, 22: 25,
        },
    },
}


def _get_current_hour(time_str: Optional[str] = None) -> int:
    """Extract hour (0-23) from time string or current time"""
    if time_str:
        try:
            hour = int(time_str.split(":")[0])
            return hour % 24
        except (ValueError, IndexError):
            pass
    return datetime.now().hour


def _interpolate_occupancy(area: str, area_type: str, hour: int) -> float:
    """
    Interpolate occupancy percentage based on historical data.
    
    Uses linear interpolation between known hours. For hours outside
    the data range, uses the nearest known value.
    """
    area_data = MOCK_HISTORICAL_OCCUPANCY.get(area, MOCK_HISTORICAL_OCCUPANCY["default"])
    type_data = area_data.get(area_type, area_data["commercial"])
    
    # Exact match
    if hour in type_data:
        return float(type_data[hour])
    
    # Find nearest hours
    known_hours = sorted(type_data.keys())
    
    # Before first known hour
    if hour < known_hours[0]:
        return float(type_data[known_hours[0]])
    
    # After last known hour
    if hour > known_hours[-1]:
        return float(type_data[known_hours[-1]])
    
    # Interpolate between two known hours
    for i in range(len(known_hours) - 1):
        h1, h2 = known_hours[i], known_hours[i + 1]
        if h1 <= hour <= h2:
            v1, v2 = type_data[h1], type_data[h2]
            # Linear interpolation
            ratio = (hour - h1) / (h2 - h1) if h2 != h1 else 0
            return float(v1 + (v2 - v1) * ratio)
    
    return 50.0  # Fallback


def _calculate_availability_level(occupancy_percent: float) -> AvailabilityLevel:
    """Convert occupancy percentage to availability level"""
    if occupancy_percent >= 80:
        return AvailabilityLevel.LOW
    elif occupancy_percent >= 50:
        return AvailabilityLevel.MEDIUM
    else:
        return AvailabilityLevel.HIGH


def _calculate_confidence(
    area: str, area_type: str, hour: int, occupancy: float
) -> float:
    """
    Calculate confidence score based on data quality and time proximity.
    
    Higher confidence when:
    - Area has historical data
    - Hour is within business hours (more predictable)
    - Occupancy is in typical range
    """
    confidence = 0.7  # Base confidence
    
    # Boost if area has specific data
    if area in MOCK_HISTORICAL_OCCUPANCY:
        confidence += 0.1
    
    # Boost if hour has direct data (not interpolated)
    area_data = MOCK_HISTORICAL_OCCUPANCY.get(area, MOCK_HISTORICAL_OCCUPANCY["default"])
    type_data = area_data.get(area_type, area_data["commercial"])
    if hour in type_data:
        confidence += 0.1
    
    # Boost for business hours (more predictable)
    if 9 <= hour <= 18:
        confidence += 0.05
    
    # Slight penalty for extreme values (less predictable)
    if occupancy < 10 or occupancy > 95:
        confidence -= 0.05
    
    return min(max(confidence, 0.5), 0.95)  # Clamp between 0.5 and 0.95


@router.get(
    "/predict",
    response_model=ParkingPredictResponse,
    summary="Predict parking availability for an area",
)
async def predict_parking_availability(
    area: str = Query(..., description="Area name (e.g., 'MG Road', 'BTM Layout')"),
    area_type: AreaType = Query(
        default=AreaType.COMMERCIAL,
        description="Type of area: commercial, residential, or mixed",
    ),
    time_of_day: Optional[str] = Query(
        default=None,
        description="Time in HH:MM format (24-hour). If not provided, uses current time.",
    ),
) -> ParkingPredictResponse:
    """
    Predict parking availability using rule-based logic.
    
    This endpoint uses:
    - **Time of day**: Peak hours (9-12, 17-19) have higher occupancy
    - **Area type**: Commercial areas peak during business hours, residential during evenings
    - **Historical patterns**: Mock historical occupancy data by hour and area type
    
    **How it works:**
    1. Looks up historical occupancy patterns for the area and time
    2. Interpolates between known data points if needed
    3. Adjusts based on area type (commercial vs residential patterns)
    4. Returns availability level (High/Medium/Low) and confidence score
    
    **Scaling to Production:**
    
    This is a rule-based predictor suitable for hackathons. To scale with real data:
    
    1. **Replace mock data with real time-series data:**
       - Store historical occupancy in a time-series DB (InfluxDB, TimescaleDB)
       - Query by area, hour, day of week, season
    
    2. **Add ML model (e.g., scikit-learn, TensorFlow):**
       ```python
       # Features: hour, day_of_week, area_type, weather, events, holidays
       # Target: occupancy_percentage
       model = RandomForestRegressor()  # or LSTM for sequences
       prediction = model.predict(features)
       ```
    
    3. **Real-time data integration:**
       - Connect to parking sensor APIs
       - Use IoT data from smart parking systems
       - Integrate with city open data portals
    
    4. **Advanced features:**
       - Weather impact (rain increases parking demand)
       - Event calendar (concerts, sports increase demand)
       - Day of week patterns (weekends differ from weekdays)
       - Seasonal trends (holiday shopping, festivals)
       - Real-time updates (webhooks from parking systems)
    
    5. **Confidence calculation:**
       - Use prediction intervals from ML models
       - Factor in data freshness and sensor reliability
       - Consider model accuracy metrics (MAE, RMSE)
    
    **Example request:**
    ```
    GET /api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=14:30
    ```
    
    **Example response:**
    ```json
    {
      "area": "MG Road",
      "availability": "Medium",
      "confidence": 0.82,
      "predicted_occupancy_percent": 75.5,
      "time_of_day": "14:30",
      "area_type": "commercial",
      "factors": {
        "base_occupancy": 85.0,
        "area_type_adjustment": 0.0,
        "time_adjustment": 0.0
      }
    }
    ```
    """
    hour = _get_current_hour(time_of_day)
    
    # Get base occupancy from historical data
    base_occupancy = _interpolate_occupancy(area, area_type.value, hour)
    
    # Apply rule-based adjustments
    adjustments = {
        "base_occupancy": base_occupancy,
        "area_type_adjustment": 0.0,
        "time_adjustment": 0.0,
    }
    
    # Peak hour adjustments
    if 9 <= hour <= 12 or 17 <= hour <= 19:
        adjustments["time_adjustment"] = 5.0  # +5% during peak hours
        base_occupancy += 5.0
    elif 20 <= hour <= 6:  # Late night/early morning
        adjustments["time_adjustment"] = -10.0  # -10% during off-peak
        base_occupancy -= 10.0
    
    # Area type adjustments
    if area_type == AreaType.RESIDENTIAL:
        # Residential areas have different patterns
        if 17 <= hour <= 21:
            adjustments["area_type_adjustment"] = 10.0  # +10% in evening
            base_occupancy += 10.0
    elif area_type == AreaType.COMMERCIAL:
        # Commercial areas peak during business hours
        if 10 <= hour <= 15:
            adjustments["area_type_adjustment"] = 5.0
            base_occupancy += 5.0
    
    # Clamp occupancy between 0 and 100
    predicted_occupancy = max(0.0, min(100.0, base_occupancy))
    
    # Calculate availability level
    availability = _calculate_availability_level(predicted_occupancy)
    
    # Calculate confidence
    confidence = _calculate_confidence(area, area_type.value, hour, predicted_occupancy)
    
    # Format time string
    if time_of_day:
        time_str = time_of_day
    else:
        now = datetime.now()
        time_str = f"{now.hour:02d}:{now.minute:02d}"
    
    return ParkingPredictResponse(
        area=area,
        availability=availability,
        confidence=round(confidence, 2),
        predicted_occupancy_percent=round(predicted_occupancy, 1),
        time_of_day=time_str,
        area_type=area_type,
        factors=adjustments,
    )


