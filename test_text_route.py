"""
Test script for the text-based route suggestion endpoint.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding for arrow characters
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

print("=" * 70)
print("Testing Text-Based Route Suggestion Endpoint")
print("=" * 70)

# Example 1: Your exact use case
print("\n[Example 1] BTM Layout to MG Road with Political Rally")
print("-" * 70)

payload_1 = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "event": "Political Rally"
}

response_1 = requests.post(
    "http://localhost:8000/api/routing/suggest",
    json=payload_1
)

if response_1.status_code == 200:
    data_1 = response_1.json()
    print(f"\nRecommended Route: {data_1['recommended_route']}")
    print(f"Reason: {data_1['reason']}")
    print(f"\nDistance: {data_1['distance_km']} km ({data_1['distance_meters']} meters)")
    print(f"Duration: {data_1['duration_minutes']} minutes ({data_1['duration_seconds']} seconds)")
    print(f"CO2 Emissions: {data_1['estimated_co2_kg']} kg")
    print(f"Waypoints: {', '.join(data_1['waypoints'])}")
    
    print("\nFull JSON Response:")
    print(json.dumps(data_1, indent=2))
else:
    print(f"[ERROR] Status: {response_1.status_code}")
    print(response_1.text)

# Example 2: Different locations
print("\n" + "=" * 70)
print("[Example 2] Whitefield to MG Road with Concert Event")
print("-" * 70)

payload_2 = {
    "source": "Whitefield",
    "destination": "MG Road",
    "event": "Concert",
    "mode": "car"
}

response_2 = requests.post(
    "http://localhost:8000/api/routing/suggest",
    json=payload_2
)

if response_2.status_code == 200:
    data_2 = response_2.json()
    print(f"\nRecommended Route: {data_2['recommended_route']}")
    print(f"Reason: {data_2['reason']}")
    print(f"\nDistance: {data_2['distance_km']} km")
    print(f"Duration: {data_2['duration_minutes']} minutes")
    print(f"CO2 Emissions: {data_2['estimated_co2_kg']} kg")
else:
    print(f"[ERROR] Status: {response_2.status_code}")
    print(response_2.text)

# Example 3: No event (normal route)
print("\n" + "=" * 70)
print("[Example 3] BTM Layout to MG Road (No Event)")
print("-" * 70)

payload_3 = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "mode": "bike"
}

response_3 = requests.post(
    "http://localhost:8000/api/routing/suggest",
    json=payload_3
)

if response_3.status_code == 200:
    data_3 = response_3.json()
    print(f"\nRecommended Route: {data_3['recommended_route']}")
    print(f"Reason: {data_3['reason']}")
    print(f"\nDistance: {data_3['distance_km']} km")
    print(f"Duration: {data_3['duration_minutes']} minutes")
    print(f"CO2 Emissions: {data_3['estimated_co2_kg']} kg (bike = zero emissions!)")
else:
    print(f"[ERROR] Status: {response_3.status_code}")
    print(response_3.text)

print("\n" + "=" * 70)
print("[OK] All tests completed!")
print("=" * 70)

