"""
Webhook endpoints for event-based alerts.
Simple, hackathon-friendly implementation for pushing notifications to partner apps.
"""
from datetime import datetime
from typing import List, Literal, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl


router = APIRouter()


# In-memory storage for registered webhooks (replace with database in production)
REGISTERED_WEBHOOKS: List[dict] = []


class WebhookEventType(str):
    """Supported webhook event types"""
    EVENT_DETECTED = "event_detected"
    PARKING_FULL = "parking_full"
    ROUTE_DISRUPTED = "route_disrupted"


class WebhookRegistration(BaseModel):
    """Request model for webhook registration"""
    url: HttpUrl = Field(..., description="Partner app webhook URL to receive notifications")
    event_types: List[str] = Field(
        ...,
        min_items=1,
        description="List of event types to subscribe to: 'event_detected', 'parking_full', 'route_disrupted'",
    )
    secret: Optional[str] = Field(
        default=None,
        description="Optional secret for webhook authentication (for production use)",
    )
    partner_name: Optional[str] = Field(
        default=None,
        description="Optional partner name for identification",
    )


class WebhookRegistrationResponse(BaseModel):
    """Response model for webhook registration"""
    webhook_id: str = Field(..., description="Unique webhook identifier")
    url: str
    event_types: List[str]
    registered_at: str
    status: str = Field(default="active", description="Webhook status: active, paused, deleted")
    message: str


class WebhookNotification(BaseModel):
    """Model for sending webhook notifications"""
    event_type: str = Field(
        ...,
        description="Type of event: 'event_detected', 'parking_full', 'route_disrupted'",
    )
    payload: dict = Field(
        ...,
        description="Event-specific payload data",
    )
    timestamp: Optional[str] = Field(
        default=None,
        description="Event timestamp (ISO8601). If not provided, uses current time.",
    )


class WebhookNotificationResponse(BaseModel):
    """Response model for webhook notification"""
    notified_count: int = Field(..., description="Number of webhooks notified")
    event_type: str
    webhooks_notified: List[dict] = Field(
        ...,
        description="List of webhooks that received the notification",
    )


class WebhookListResponse(BaseModel):
    """Response model for listing webhooks"""
    total: int
    webhooks: List[dict]


@router.post(
    "/register",
    response_model=WebhookRegistrationResponse,
    summary="Register a webhook for event notifications",
)
async def register_webhook(payload: WebhookRegistration) -> WebhookRegistrationResponse:
    """
    Register a webhook URL to receive event-based notifications.
    
    **Supported Event Types:**
    - `event_detected`: New mobility event detected (protests, concerts, etc.)
    - `parking_full`: Parking area reached full capacity
    - `route_disrupted`: Route disruption detected (road closures, accidents, etc.)
    
    **Example Request:**
    ```json
    {
      "url": "https://partner-app.com/webhook",
      "event_types": ["event_detected", "parking_full"],
      "partner_name": "City Traffic App",
      "secret": "optional-secret-key"
    }
    ```
    
    **Example Response:**
    ```json
    {
      "webhook_id": "wh_abc123",
      "url": "https://partner-app.com/webhook",
      "event_types": ["event_detected", "parking_full"],
      "registered_at": "2024-01-15T10:30:00Z",
      "status": "active",
      "message": "Webhook registered successfully"
    }
    ```
    
    **Production Notes:**
    - Store webhooks in a database (PostgreSQL, MongoDB)
    - Implement webhook signature verification using the secret
    - Add rate limiting and retry logic
    - Support webhook status management (pause, resume, delete)
    """
    webhook_id = f"wh_{uuid4().hex[:12]}"
    
    webhook_data = {
        "webhook_id": webhook_id,
        "url": str(payload.url),
        "event_types": payload.event_types,
        "secret": payload.secret,
        "partner_name": payload.partner_name,
        "registered_at": datetime.utcnow().isoformat() + "Z",
        "status": "active",
    }
    
    REGISTERED_WEBHOOKS.append(webhook_data)
    
    return WebhookRegistrationResponse(
        webhook_id=webhook_id,
        url=str(payload.url),
        event_types=payload.event_types,
        registered_at=webhook_data["registered_at"],
        status="active",
        message="Webhook registered successfully",
    )


@router.post(
    "/notify",
    response_model=WebhookNotificationResponse,
    summary="Send notification to registered webhooks",
)
async def notify_webhooks(payload: WebhookNotification) -> WebhookNotificationResponse:
    """
    Send a notification to all webhooks subscribed to the specified event type.
    
    **Event Types:**
    - `event_detected`: New mobility event
    - `parking_full`: Parking area full
    - `route_disrupted`: Route disruption
    
    **Example Request:**
    ```json
    {
      "event_type": "parking_full",
      "payload": {
        "area": "MG Road",
        "capacity": 150,
        "occupied": 150,
        "timestamp": "2024-01-15T10:30:00Z"
      }
    }
    ```
    
    **Example Response:**
    ```json
    {
      "notified_count": 2,
      "event_type": "parking_full",
      "webhooks_notified": [
        {
          "webhook_id": "wh_abc123",
          "url": "https://partner-app.com/webhook",
          "status": "sent"
        }
      ]
    }
    ```
    
    **Production Notes:**
    - Use async HTTP client (httpx) for non-blocking requests
    - Implement retry logic with exponential backoff
    - Add webhook signature headers for security
    - Log delivery status and failures
    - Queue notifications for high-volume scenarios
    """
    timestamp = payload.timestamp or datetime.utcnow().isoformat() + "Z"
    
    # Find webhooks subscribed to this event type
    matching_webhooks = [
        wh for wh in REGISTERED_WEBHOOKS
        if wh["status"] == "active" and payload.event_type in wh["event_types"]
    ]
    
    if not matching_webhooks:
        return WebhookNotificationResponse(
            notified_count=0,
            event_type=payload.event_type,
            webhooks_notified=[],
        )
    
    # In a real implementation, you would make HTTP POST requests here
    # For hackathon, we'll just simulate and return the list
    notified_webhooks = []
    
    for webhook in matching_webhooks:
        # In production, make actual HTTP request:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         webhook["url"],
        #         json={
        #             "event_type": payload.event_type,
        #             "payload": payload.payload,
        #             "timestamp": timestamp,
        #         },
        #         headers={
        #             "X-Webhook-Signature": compute_signature(webhook["secret"], payload),
        #         },
        #         timeout=5.0,
        #     )
        
        notified_webhooks.append({
            "webhook_id": webhook["webhook_id"],
            "url": webhook["url"],
            "partner_name": webhook.get("partner_name"),
            "status": "sent",  # In production: "sent", "failed", "retrying"
        })
    
    return WebhookNotificationResponse(
        notified_count=len(notified_webhooks),
        event_type=payload.event_type,
        webhooks_notified=notified_webhooks,
    )


@router.get(
    "/list",
    response_model=WebhookListResponse,
    summary="List all registered webhooks",
)
async def list_webhooks() -> WebhookListResponse:
    """
    List all registered webhooks.
    
    Useful for debugging and monitoring during hackathons.
    """
    return WebhookListResponse(
        total=len(REGISTERED_WEBHOOKS),
        webhooks=REGISTERED_WEBHOOKS,
    )


@router.delete(
    "/{webhook_id}",
    summary="Delete a registered webhook",
)
async def delete_webhook(webhook_id: str) -> dict:
    """
    Delete a webhook by ID.
    
    In production, mark as deleted rather than removing from database.
    """
    global REGISTERED_WEBHOOKS
    
    initial_count = len(REGISTERED_WEBHOOKS)
    REGISTERED_WEBHOOKS = [
        wh for wh in REGISTERED_WEBHOOKS if wh["webhook_id"] != webhook_id
    ]
    
    if len(REGISTERED_WEBHOOKS) < initial_count:
        return {"message": f"Webhook {webhook_id} deleted successfully", "deleted": True}
    else:
        raise HTTPException(status_code=404, detail=f"Webhook {webhook_id} not found")

