from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field


router = APIRouter()


class MobilityEvent(BaseModel):
    id: str
    title: str
    category: str = Field(
        description="Type of event, e.g. 'road_closure', 'concert', 'protest', 'sports'."
    )
    lat: float
    lon: float
    starts_at: datetime
    ends_at: datetime
    description: Optional[str] = None
    severity: int = Field(
        1,
        ge=1,
        le=5,
        description="Impact level from 1 (low) to 5 (high).",
    )


class EventsResponse(BaseModel):
    items: List[MobilityEvent]
    count: int
    center_lat: float
    center_lon: float
    radius_km: int


def _mock_events(now: datetime) -> List[MobilityEvent]:
    return [
        MobilityEvent(
            id="e1",
            title="Road maintenance near central hub",
            category="road_closure",
            lat=12.9716,
            lon=77.5946,
            starts_at=now - timedelta(hours=1),
            ends_at=now + timedelta(hours=5),
            description="One lane closed, expect moderate delays.",
            severity=3,
        ),
        MobilityEvent(
            id="e2",
            title="Stadium football match",
            category="sports",
            lat=12.9352,
            lon=77.6245,
            starts_at=now + timedelta(hours=2),
            ends_at=now + timedelta(hours=6),
            description="High traffic expected pre- and post-match.",
            severity=4,
        ),
    ]


@router.get(
    "/nearby",
    response_model=EventsResponse,
    summary="Get mobility-impacting events near a location",
)
async def get_nearby_events(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_km: int = Query(
        5,
        ge=1,
        le=50,
        description="Search radius in kilometers. Defaults to 5km.",
    ),
    active_only: bool = Query(
        True,
        description="If true, only return events that are ongoing or starting soon.",
    ),
) -> EventsResponse:
    """
    Fetch mobility-impacting events near a location.

    Currently powered by in-memory mock data so it works instantly in
    hackathon settings. Replace `_mock_events` with your own datasource
    (e.g. city feeds, crowd-sourced reports, or a database).
    """
    now = datetime.now(timezone.utc)
    events = _mock_events(now)

    if active_only:
        events = [
            e
            for e in events
            if e.starts_at <= now <= e.ends_at or (e.starts_at - now).total_seconds() <= 3 * 3600
        ]

    return EventsResponse(
        items=events,
        count=len(events),
        center_lat=lat,
        center_lon=lon,
        radius_km=radius_km,
    )


