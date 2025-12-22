# Webhook API - Test Examples

Quick reference for testing the webhook endpoints for event-based alerts.

## Base URLs
```
POST /api/webhook/register  - Register a webhook
POST /api/webhook/notify     - Send notification to webhooks
GET  /api/webhook/list       - List all registered webhooks
DELETE /api/webhook/{id}     - Delete a webhook
```

## Supported Event Types

- `event_detected` - New mobility event detected (protests, concerts, etc.)
- `parking_full` - Parking area reached full capacity
- `route_disrupted` - Route disruption detected (road closures, accidents, etc.)

## Example 1: Register Webhook for Event Detection

**Request:**
```json
POST /api/webhook/register
{
  "url": "https://partner-app.com/webhooks/events",
  "event_types": ["event_detected"],
  "partner_name": "City Traffic App",
  "secret": "secret-key-123"
}
```

**Response:**
```json
{
  "webhook_id": "wh_abc123",
  "url": "https://partner-app.com/webhooks/events",
  "event_types": ["event_detected"],
  "registered_at": "2024-01-15T10:30:00Z",
  "status": "active",
  "message": "Webhook registered successfully"
}
```

## Example 2: Register Webhook for Parking Full

**Request:**
```json
POST /api/webhook/register
{
  "url": "https://parking-service.com/webhook",
  "event_types": ["parking_full"],
  "partner_name": "Parking Management System"
}
```

## Example 3: Register Webhook for Multiple Events

**Request:**
```json
POST /api/webhook/register
{
  "url": "https://mobility-platform.com/webhooks",
  "event_types": ["event_detected", "parking_full", "route_disrupted"],
  "partner_name": "Mobility Intelligence Platform"
}
```

## Example 4: Notify - Event Detected

**Request:**
```json
POST /api/webhook/notify
{
  "event_type": "event_detected",
  "payload": {
    "event_id": "evt_123",
    "event_type": "protest",
    "location": {
      "area": "MG Road",
      "lat": 12.9716,
      "lon": 77.5946
    },
    "description": "Political rally detected near MG Road",
    "severity": "medium",
    "estimated_duration": "2 hours"
  }
}
```

**Response:**
```json
{
  "notified_count": 2,
  "event_type": "event_detected",
  "webhooks_notified": [
    {
      "webhook_id": "wh_abc123",
      "url": "https://partner-app.com/webhooks/events",
      "partner_name": "City Traffic App",
      "status": "sent"
    }
  ]
}
```

## Example 5: Notify - Parking Full

**Request:**
```json
POST /api/webhook/notify
{
  "event_type": "parking_full",
  "payload": {
    "area": "MG Road",
    "parking_id": "p1",
    "capacity": 150,
    "occupied": 150,
    "available": 0,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Example 6: Notify - Route Disrupted

**Request:**
```json
POST /api/webhook/notify
{
  "event_type": "route_disrupted",
  "payload": {
    "route_id": "route_456",
    "disruption_type": "road_closure",
    "location": {
      "area": "BTM Layout",
      "lat": 12.9166,
      "lon": 77.6101
    },
    "reason": "Construction work",
    "estimated_delay": "15 minutes",
    "alternate_routes": [
      "BTM → JP Nagar → Richmond Road"
    ]
  }
}
```

## PowerShell Examples

### Register Webhook
```powershell
$body = @{
    url = "https://partner-app.com/webhooks/events"
    event_types = @("event_detected")
    partner_name = "City Traffic App"
    secret = "secret-key-123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/webhook/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Notify Webhooks
```powershell
$body = @{
    event_type = "parking_full"
    payload = @{
        area = "MG Road"
        parking_id = "p1"
        capacity = 150
        occupied = 150
        available = 0
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/webhook/notify" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### List All Webhooks
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/webhook/list" -Method GET
```

### Delete Webhook
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/webhook/wh_abc123" -Method DELETE
```

## Python Examples

### Register Webhook
```python
import requests

response = requests.post(
    "http://localhost:8000/api/webhook/register",
    json={
        "url": "https://partner-app.com/webhooks/events",
        "event_types": ["event_detected"],
        "partner_name": "City Traffic App",
        "secret": "secret-key-123"
    }
)
print(response.json())
```

### Notify Webhooks
```python
import requests

response = requests.post(
    "http://localhost:8000/api/webhook/notify",
    json={
        "event_type": "parking_full",
        "payload": {
            "area": "MG Road",
            "parking_id": "p1",
            "capacity": 150,
            "occupied": 150,
            "available": 0
        }
    }
)
print(response.json())
```

## Use Cases

### Use Case 1: Event Detected
When a new mobility event is detected (protest, concert, etc.), notify all webhooks subscribed to `event_detected`.

### Use Case 2: Parking Full
When a parking area reaches full capacity, notify all webhooks subscribed to `parking_full`.

### Use Case 3: Route Disrupted
When a route disruption is detected (road closure, accident, etc.), notify all webhooks subscribed to `route_disrupted`.

## Production Notes

⚠️ **This is a mock implementation for hackathons.** In production:

1. **Make actual HTTP requests** to registered webhook URLs
2. **Store webhooks in a database** (PostgreSQL, MongoDB)
3. **Implement retry logic** with exponential backoff
4. **Add webhook signature verification** using the secret
5. **Queue notifications** for high-volume scenarios
6. **Log delivery status** and failures
7. **Support webhook status management** (pause, resume, delete)

### Example Production Implementation

```python
import httpx

async def notify_webhook(webhook_url: str, payload: dict, secret: str):
    async with httpx.AsyncClient() as client:
        signature = compute_signature(secret, payload)
        response = await client.post(
            webhook_url,
            json=payload,
            headers={"X-Webhook-Signature": signature},
            timeout=5.0,
        )
        return response.status_code == 200
```

## Testing Tips

1. **Use Swagger UI**: Visit `http://localhost:8000/docs` for interactive testing
2. **Register multiple webhooks**: Test with different event types
3. **Test notifications**: Send notifications and verify all subscribed webhooks are notified
4. **Test deletion**: Delete webhooks and verify they're removed
5. **Test edge cases**: Notify events with no subscribers

