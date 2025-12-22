"""
Simple test examples for the parking availability predictor.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

BASE_URL = "http://localhost:8000/api/parking/predict"

print("=" * 80)
print("PARKING AVAILABILITY PREDICTOR - Quick Test Examples")
print("=" * 80)

# Example 1: Your exact use case from the requirements
print("\n" + "=" * 80)
print("Example 1: MG Road - Commercial - Peak Hours")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=MG Road&area_type=commercial&time_of_day=10:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
    print(f"\n[INFO] Summary:")
    print(f"   Area: {data['area']}")
    print(f"   Availability: {data['availability']}")
    print(f"   Confidence: {data['confidence']}")
    print(f"   Occupancy: {data['predicted_occupancy_percent']}%")
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 2: Residential area in evening
print("\n" + "=" * 80)
print("Example 2: BTM Layout - Residential - Evening")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=BTM Layout&area_type=residential&time_of_day=19:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 3: Mixed area type
print("\n" + "=" * 80)
print("Example 3: MG Road - Mixed Area - Afternoon")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=MG Road&area_type=mixed&time_of_day=15:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 4: Late night (should be high availability)
print("\n" + "=" * 80)
print("Example 4: MG Road - Commercial - Late Night")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=MG Road&area_type=commercial&time_of_day=23:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 5: Early morning
print("\n" + "=" * 80)
print("Example 5: BTM Layout - Commercial - Early Morning")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=BTM Layout&area_type=commercial&time_of_day=08:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 6: Current time (no time specified)
print("\n" + "=" * 80)
print("Example 6: MG Road - Commercial - Current Time")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=MG Road&area_type=commercial")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 7: Lunch peak
print("\n" + "=" * 80)
print("Example 7: MG Road - Commercial - Lunch Peak")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=MG Road&area_type=commercial&time_of_day=12:30")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

# Example 8: Unknown area (uses default pattern)
print("\n" + "=" * 80)
print("Example 8: New Area - Commercial - Peak Hours")
print("=" * 80)
r = requests.get(f"{BASE_URL}?area=Koramangala&area_type=commercial&time_of_day=11:00")
if r.status_code == 200:
    data = r.json()
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r.status_code} - {r.text}")

print("\n" + "=" * 80)
print("[OK] All examples completed!")
print("=" * 80)
print("\n[INFO] Tip: Visit http://localhost:8000/docs for interactive testing")

