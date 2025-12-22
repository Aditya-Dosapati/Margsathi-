"""
Comprehensive examples for the text-based route suggestion endpoint.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding for arrow characters
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


def print_example(num, title, payload, response):
    """Helper function to print formatted examples"""
    print("\n" + "=" * 70)
    print(f"[Example {num}] {title}")
    print("-" * 70)
    print(f"\nRequest JSON:")
    print(json.dumps(payload, indent=2))
    print(f"\nResponse:")
    print(f"  Route: {response['recommended_route']}")
    print(f"  Reason: {response['reason']}")
    print(f"  Distance: {response['distance_km']} km ({response['distance_meters']:.0f} m)")
    print(f"  Duration: {response['duration_minutes']:.1f} min ({response['duration_seconds']:.0f} sec)")
    print(f"  CO2: {response['estimated_co2_kg']} kg")
    print(f"  Waypoints: {' → '.join(response['waypoints'])}")


print("=" * 70)
print("COMPREHENSIVE EXAMPLES - Text-Based Route Suggestion API")
print("=" * 70)

base_url = "http://localhost:8000/api/routing/suggest"

# Example 1: Road Closure Event
payload_1 = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "event": "Road Closure",
    "mode": "car"
}
r1 = requests.post(base_url, json=payload_1)
if r1.status_code == 200:
    print_example(1, "Road Closure Event", payload_1, r1.json())

# Example 2: Accident on Route
payload_2 = {
    "source": "Whitefield",
    "destination": "MG Road",
    "event": "Accident",
    "mode": "car"
}
r2 = requests.post(base_url, json=payload_2)
if r2.status_code == 200:
    print_example(2, "Accident Avoidance", payload_2, r2.json())

# Example 3: Sports Event
payload_3 = {
    "source": "Indiranagar",
    "destination": "MG Road",
    "event": "Sports Event",
    "mode": "car"
}
r3 = requests.post(base_url, json=payload_3)
if r3.status_code == 200:
    print_example(3, "Sports Event Traffic", payload_3, r3.json())

# Example 4: Construction Work
payload_4 = {
    "source": "Electronic City",
    "destination": "MG Road",
    "event": "Construction",
    "mode": "car"
}
r4 = requests.post(base_url, json=payload_4)
if r4.status_code == 200:
    print_example(4, "Construction Detour", payload_4, r4.json())

# Example 5: Bike Mode (Zero Emissions)
payload_5 = {
    "source": "BTM Layout",
    "destination": "Koramangala",
    "event": "",
    "mode": "bike"
}
r5 = requests.post(base_url, json=payload_5)
if r5.status_code == 200:
    print_example(5, "Bike Route (Eco-Friendly)", payload_5, r5.json())

# Example 6: Walking Route
payload_6 = {
    "source": "JP Nagar",
    "destination": "Richmond Road",
    "event": "",
    "mode": "walk"
}
r6 = requests.post(base_url, json=payload_6)
if r6.status_code == 200:
    print_example(6, "Walking Route", payload_6, r6.json())

# Example 7: Transit Mode
payload_7 = {
    "source": "Hebbal",
    "destination": "MG Road",
    "event": "",
    "mode": "transit"
}
r7 = requests.post(base_url, json=payload_7)
if r7.status_code == 200:
    print_example(7, "Public Transit Route", payload_7, r7.json())

# Example 8: Protest/Rally
payload_8 = {
    "source": "Malleshwaram",
    "destination": "MG Road",
    "event": "Protest",
    "mode": "car"
}
r8 = requests.post(base_url, json=payload_8)
if r8.status_code == 200:
    print_example(8, "Protest Avoidance", payload_8, r8.json())

# Example 9: Parade Event
payload_9 = {
    "source": "Rajajinagar",
    "destination": "Cubbon Park",
    "event": "Parade",
    "mode": "car"
}
r9 = requests.post(base_url, json=payload_9)
if r9.status_code == 200:
    print_example(9, "Parade Route Adjustment", payload_9, r9.json())

# Example 10: Concert Event
payload_10 = {
    "source": "Ulsoor",
    "destination": "MG Road",
    "event": "Concert",
    "mode": "car"
}
r10 = requests.post(base_url, json=payload_10)
if r10.status_code == 200:
    print_example(10, "Concert Traffic Avoidance", payload_10, r10.json())

# Example 11: No Event (Normal Route)
payload_11 = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "event": "",
    "mode": "car"
}
r11 = requests.post(base_url, json=payload_11)
if r11.status_code == 200:
    print_example(11, "Normal Route (No Events)", payload_11, r11.json())

# Example 12: Long Distance Route
payload_12 = {
    "source": "Whitefield",
    "destination": "Electronic City",
    "event": "Heavy Traffic",
    "mode": "car"
}
r12 = requests.post(base_url, json=payload_12)
if r12.status_code == 200:
    print_example(12, "Long Distance Route", payload_12, r12.json())

# Example 13: Political Rally (Your Original Use Case)
payload_13 = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "event": "Political Rally",
    "mode": "car"
}
r13 = requests.post(base_url, json=payload_13)
if r13.status_code == 200:
    print_example(13, "Political Rally (Original Example)", payload_13, r13.json())

# Example 14: Multiple Events Comparison
print("\n" + "=" * 70)
print("[Comparison] Same Route with Different Events")
print("-" * 70)

base_payload = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "mode": "car"
}

events = [
    ("No Event", ""),
    ("Road Closure", "Road Closure"),
    ("Protest", "Protest"),
    ("Concert", "Concert"),
]

print("\nRoute: BTM Layout → MG Road")
print("\nEvent Impact Comparison:")
print("-" * 70)
for event_name, event_value in events:
    test_payload = {**base_payload, "event": event_value}
    r = requests.post(base_url, json=test_payload)
    if r.status_code == 200:
        data = r.json()
        print(f"\n{event_name}:")
        print(f"  Distance: {data['distance_km']:.2f} km")
        print(f"  Duration: {data['duration_minutes']:.1f} min")
        print(f"  Reason: {data['reason']}")

# Example 15: Different Travel Modes Comparison
print("\n" + "=" * 70)
print("[Comparison] Same Route with Different Travel Modes")
print("-" * 70)

base_payload_mode = {
    "source": "BTM Layout",
    "destination": "MG Road",
    "event": ""
}

modes = ["car", "bike", "walk", "transit"]

print("\nRoute: BTM Layout → MG Road (No Events)")
print("\nMode Comparison:")
print("-" * 70)
for mode in modes:
    test_payload = {**base_payload_mode, "mode": mode}
    r = requests.post(base_url, json=test_payload)
    if r.status_code == 200:
        data = r.json()
        print(f"\n{mode.upper()}:")
        print(f"  Distance: {data['distance_km']:.2f} km")
        print(f"  Duration: {data['duration_minutes']:.1f} min")
        print(f"  CO2: {data['estimated_co2_kg']} kg")

print("\n" + "=" * 70)
print("[OK] All examples completed!")
print("=" * 70)
print("\nTip: Visit http://localhost:8000/docs for interactive API testing")

