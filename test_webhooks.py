"""
Test examples for webhook endpoints.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

BASE_URL = "http://localhost:8000/api/webhook"

print("=" * 80)
print("WEBHOOK API - Test Examples")
print("=" * 80)

# Example 1: Register webhook for event_detected
print("\n" + "=" * 80)
print("Example 1: Register Webhook for Event Detection")
print("=" * 80)
payload_1 = {
    "url": "https://partner-app.com/webhooks/events",
    "event_types": ["event_detected"],
    "partner_name": "City Traffic App",
    "secret": "secret-key-123"
}
r1 = requests.post(f"{BASE_URL}/register", json=payload_1)
if r1.status_code == 200:
    data_1 = r1.json()
    webhook_id_1 = data_1["webhook_id"]
    print(f"\n[OK] Request:")
    print(json.dumps(payload_1, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_1, indent=2))
    print(f"\n[INFO] Webhook ID: {webhook_id_1}")
else:
    print(f"[ERROR] Error: {r1.status_code} - {r1.text}")
    webhook_id_1 = None

# Example 2: Register webhook for parking_full
print("\n" + "=" * 80)
print("Example 2: Register Webhook for Parking Full Alerts")
print("=" * 80)
payload_2 = {
    "url": "https://parking-service.com/webhook",
    "event_types": ["parking_full"],
    "partner_name": "Parking Management System"
}
r2 = requests.post(f"{BASE_URL}/register", json=payload_2)
if r2.status_code == 200:
    data_2 = r2.json()
    webhook_id_2 = data_2["webhook_id"]
    print(f"\n[OK] Request:")
    print(json.dumps(payload_2, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_2, indent=2))
    print(f"\n[INFO] Webhook ID: {webhook_id_2}")
else:
    print(f"[ERROR] Error: {r2.status_code} - {r2.text}")
    webhook_id_2 = None

# Example 3: Register webhook for multiple event types
print("\n" + "=" * 80)
print("Example 3: Register Webhook for Multiple Event Types")
print("=" * 80)
payload_3 = {
    "url": "https://mobility-platform.com/webhooks",
    "event_types": ["event_detected", "parking_full", "route_disrupted"],
    "partner_name": "Mobility Intelligence Platform"
}
r3 = requests.post(f"{BASE_URL}/register", json=payload_3)
if r3.status_code == 200:
    data_3 = r3.json()
    webhook_id_3 = data_3["webhook_id"]
    print(f"\n[OK] Request:")
    print(json.dumps(payload_3, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_3, indent=2))
    print(f"\n[INFO] Webhook ID: {webhook_id_3}")
else:
    print(f"[ERROR] Error: {r3.status_code} - {r3.text}")
    webhook_id_3 = None

# Example 4: List all registered webhooks
print("\n" + "=" * 80)
print("Example 4: List All Registered Webhooks")
print("=" * 80)
r4 = requests.get(f"{BASE_URL}/list")
if r4.status_code == 200:
    data_4 = r4.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data_4, indent=2))
    print(f"\n[INFO] Total webhooks registered: {data_4['total']}")
else:
    print(f"[ERROR] Error: {r4.status_code} - {r4.text}")

# Example 5: Notify - Event Detected
print("\n" + "=" * 80)
print("Example 5: Notify - Event Detected")
print("=" * 80)
payload_5 = {
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
r5 = requests.post(f"{BASE_URL}/notify", json=payload_5)
if r5.status_code == 200:
    data_5 = r5.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_5, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_5, indent=2))
    print(f"\n[INFO] Notified {data_5['notified_count']} webhook(s)")
else:
    print(f"[ERROR] Error: {r5.status_code} - {r5.text}")

# Example 6: Notify - Parking Full
print("\n" + "=" * 80)
print("Example 6: Notify - Parking Full")
print("=" * 80)
payload_6 = {
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
r6 = requests.post(f"{BASE_URL}/notify", json=payload_6)
if r6.status_code == 200:
    data_6 = r6.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_6, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_6, indent=2))
    print(f"\n[INFO] Notified {data_6['notified_count']} webhook(s)")
else:
    print(f"[ERROR] Error: {r6.status_code} - {r6.text}")

# Example 7: Notify - Route Disrupted
print("\n" + "=" * 80)
print("Example 7: Notify - Route Disrupted")
print("=" * 80)
payload_7 = {
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
r7 = requests.post(f"{BASE_URL}/notify", json=payload_7)
if r7.status_code == 200:
    data_7 = r7.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_7, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_7, indent=2))
    print(f"\n[INFO] Notified {data_7['notified_count']} webhook(s)")
else:
    print(f"[ERROR] Error: {r7.status_code} - {r7.text}")

# Example 8: Delete a webhook
if webhook_id_1:
    print("\n" + "=" * 80)
    print("Example 8: Delete Webhook")
    print("=" * 80)
    r8 = requests.delete(f"{BASE_URL}/{webhook_id_1}")
    if r8.status_code == 200:
        data_8 = r8.json()
        print(f"\n[OK] Response:")
        print(json.dumps(data_8, indent=2))
    else:
        print(f"[ERROR] Error: {r8.status_code} - {r8.text}")

# Example 9: Verify webhook was deleted
print("\n" + "=" * 80)
print("Example 9: Verify Webhook Deletion")
print("=" * 80)
r9 = requests.get(f"{BASE_URL}/list")
if r9.status_code == 200:
    data_9 = r9.json()
    print(f"\n[OK] Total webhooks remaining: {data_9['total']}")
    print(f"[INFO] Webhooks:")
    for wh in data_9['webhooks']:
        print(f"  - {wh['webhook_id']}: {wh['url']} ({', '.join(wh['event_types'])})")
else:
    print(f"[ERROR] Error: {r9.status_code} - {r9.text}")

# Example 10: Notify with no subscribers
print("\n" + "=" * 80)
print("Example 10: Notify Event with No Subscribers")
print("=" * 80)
payload_10 = {
    "event_type": "event_detected",
    "payload": {
        "test": "This event has no subscribers"
    }
}
r10 = requests.post(f"{BASE_URL}/notify", json=payload_10)
if r10.status_code == 200:
    data_10 = r10.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_10, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data_10, indent=2))
    print(f"\n[INFO] Notified {data_10['notified_count']} webhook(s) (expected: 0)")
else:
    print(f"[ERROR] Error: {r10.status_code} - {r10.text}")

print("\n" + "=" * 80)
print("[OK] All examples completed!")
print("=" * 80)
print("\n[INFO] Tip: Visit http://localhost:8000/docs for interactive API testing")
print("\n[INFO] Note: In production, webhooks would make actual HTTP POST requests")
print("       to the registered URLs. This is a mock implementation for hackathons.")

