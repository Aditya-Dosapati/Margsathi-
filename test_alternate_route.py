"""
Quick test script to demonstrate the alternate route endpoint.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json

# Example 1: Road closure event (30% multiplier)
print("=" * 60)
print("Example 1: Road Closure Event")
print("=" * 60)

payload_1 = {
    "origin": {"lat": 12.9716, "lon": 77.5946},  # Bangalore coordinates
    "destination": {"lat": 12.9352, "lon": 77.6245},  # Another point in Bangalore
    "mode": "car",
    "event_type": "road_closure"
}

response_1 = requests.post(
    "http://localhost:8000/api/routing/plan/alternate",
    json=payload_1
)

if response_1.status_code == 200:
    data_1 = response_1.json()
    print(f"\n[OK] Base Route:")
    print(f"   Distance: {data_1['base_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_1['base_route']['summary']['duration_seconds']:.1f} seconds ({data_1['base_route']['summary']['duration_seconds']/60:.1f} minutes)")
    print(f"   CO2: {data_1['base_route']['summary']['estimated_co2_kg']:.3f} kg")
    
    print(f"\n[OK] Alternate Route (with {data_1['alternate_route']['debug']['multiplier']}x multiplier):")
    print(f"   Distance: {data_1['alternate_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_1['alternate_route']['summary']['duration_seconds']:.1f} seconds ({data_1['alternate_route']['summary']['duration_seconds']/60:.1f} minutes)")
    print(f"   CO2: {data_1['alternate_route']['summary']['estimated_co2_kg']:.3f} kg")
    
    print(f"\n[INFO] Reasoning: {data_1['reasoning']}")
else:
    print(f"[ERROR] Error: {response_1.status_code}")
    print(response_1.text)

# Example 2: Protest event (20% multiplier)
print("\n" + "=" * 60)
print("Example 2: Protest Event")
print("=" * 60)

payload_2 = {
    "origin": {"lat": 12.9716, "lon": 77.5946},
    "destination": {"lat": 12.9352, "lon": 77.6245},
    "mode": "car",
    "event_type": "protest"
}

response_2 = requests.post(
    "http://localhost:8000/api/routing/plan/alternate",
    json=payload_2
)

if response_2.status_code == 200:
    data_2 = response_2.json()
    print(f"\n[OK] Base Route:")
    print(f"   Distance: {data_2['base_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_2['base_route']['summary']['duration_seconds']:.1f} seconds ({data_2['base_route']['summary']['duration_seconds']/60:.1f} minutes)")
    
    print(f"\n[OK] Alternate Route (with {data_2['alternate_route']['debug']['multiplier']}x multiplier):")
    print(f"   Distance: {data_2['alternate_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_2['alternate_route']['summary']['duration_seconds']:.1f} seconds ({data_2['alternate_route']['summary']['duration_seconds']/60:.1f} minutes)")
    
    print(f"\n[INFO] Reasoning: {data_2['reasoning']}")
else:
    print(f"[ERROR] Error: {response_2.status_code}")
    print(response_2.text)

# Example 3: Concert event (15% multiplier)
print("\n" + "=" * 60)
print("Example 3: Concert Event")
print("=" * 60)

payload_3 = {
    "origin": {"lat": 12.9716, "lon": 77.5946},
    "destination": {"lat": 12.9352, "lon": 77.6245},
    "mode": "bike",
    "event_type": "concert"
}

response_3 = requests.post(
    "http://localhost:8000/api/routing/plan/alternate",
    json=payload_3
)

if response_3.status_code == 200:
    data_3 = response_3.json()
    print(f"\n[OK] Base Route (by bike):")
    print(f"   Distance: {data_3['base_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_3['base_route']['summary']['duration_seconds']:.1f} seconds ({data_3['base_route']['summary']['duration_seconds']/60:.1f} minutes)")
    print(f"   CO2: {data_3['base_route']['summary']['estimated_co2_kg']:.3f} kg")
    
    print(f"\n[OK] Alternate Route (with {data_3['alternate_route']['debug']['multiplier']}x multiplier):")
    print(f"   Distance: {data_3['alternate_route']['summary']['distance_meters']:.2f} meters")
    print(f"   Duration: {data_3['alternate_route']['summary']['duration_seconds']:.1f} seconds ({data_3['alternate_route']['summary']['duration_seconds']/60:.1f} minutes)")
    print(f"   CO2: {data_3['alternate_route']['summary']['estimated_co2_kg']:.3f} kg")
    
    print(f"\n[INFO] Reasoning: {data_3['reasoning']}")
else:
    print(f"[ERROR] Error: {response_3.status_code}")
    print(response_3.text)

print("\n" + "=" * 60)
print("[OK] All examples completed!")
print("=" * 60)

