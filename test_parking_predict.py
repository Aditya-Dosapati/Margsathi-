"""
Test script for the parking availability predictor endpoint.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


def print_prediction(title, response_data):
    """Helper to print formatted prediction results"""
    print(f"\n{title}")
    print("-" * 70)
    print(f"Area: {response_data['area']}")
    print(f"Availability: {response_data['availability']}")
    print(f"Confidence: {response_data['confidence']}")
    print(f"Predicted Occupancy: {response_data['predicted_occupancy_percent']}%")
    print(f"Time: {response_data['time_of_day']}")
    print(f"Area Type: {response_data['area_type']}")
    print(f"\nFactors:")
    for key, value in response_data['factors'].items():
        print(f"  {key}: {value}")


print("=" * 70)
print("Parking Availability Predictor - Test Examples")
print("=" * 70)

base_url = "http://localhost:8000/api/parking/predict"

# Example 1: MG Road, Commercial, Peak Hours
print("\n[Example 1] MG Road - Commercial Area - Peak Hours (10:00)")
r1 = requests.get(f"{base_url}?area=MG Road&area_type=commercial&time_of_day=10:00")
if r1.status_code == 200:
    print_prediction("MG Road (Commercial) at 10:00 AM", r1.json())
else:
    print(f"Error: {r1.status_code} - {r1.text}")

# Example 2: MG Road, Commercial, Off-Peak
print("\n[Example 2] MG Road - Commercial Area - Off-Peak (22:00)")
r2 = requests.get(f"{base_url}?area=MG Road&area_type=commercial&time_of_day=22:00")
if r2.status_code == 200:
    print_prediction("MG Road (Commercial) at 10:00 PM", r2.json())
else:
    print(f"Error: {r2.status_code} - {r2.text}")

# Example 3: BTM Layout, Residential, Evening
print("\n[Example 3] BTM Layout - Residential Area - Evening (19:00)")
r3 = requests.get(f"{base_url}?area=BTM Layout&area_type=residential&time_of_day=19:00")
if r3.status_code == 200:
    print_prediction("BTM Layout (Residential) at 7:00 PM", r3.json())
else:
    print(f"Error: {r3.status_code} - {r3.text}")

# Example 4: BTM Layout, Commercial, Lunch Time
print("\n[Example 4] BTM Layout - Commercial Area - Lunch Time (12:30)")
r4 = requests.get(f"{base_url}?area=BTM Layout&area_type=commercial&time_of_day=12:30")
if r4.status_code == 200:
    print_prediction("BTM Layout (Commercial) at 12:30 PM", r4.json())
else:
    print(f"Error: {r4.status_code} - {r4.text}")

# Example 5: Mixed Area Type
print("\n[Example 5] MG Road - Mixed Area - Afternoon (15:00)")
r5 = requests.get(f"{base_url}?area=MG Road&area_type=mixed&time_of_day=15:00")
if r5.status_code == 200:
    print_prediction("MG Road (Mixed) at 3:00 PM", r5.json())
else:
    print(f"Error: {r5.status_code} - {r5.text}")

# Example 6: Current Time (no time specified)
print("\n[Example 6] MG Road - Commercial - Current Time")
r6 = requests.get(f"{base_url}?area=MG Road&area_type=commercial")
if r6.status_code == 200:
    print_prediction("MG Road (Commercial) - Current Time", r6.json())
else:
    print(f"Error: {r6.status_code} - {r6.text}")

# Example 7: Unknown Area (uses default pattern)
print("\n[Example 7] Unknown Area - Commercial - Peak Hours")
r7 = requests.get(f"{base_url}?area=New Area&area_type=commercial&time_of_day=11:00")
if r7.status_code == 200:
    print_prediction("New Area (Commercial) at 11:00 AM", r7.json())
else:
    print(f"Error: {r7.status_code} - {r7.text}")

# Comparison: Same area, different times
print("\n" + "=" * 70)
print("[Comparison] MG Road (Commercial) - Different Times of Day")
print("-" * 70)

times = [
    ("Early Morning", "08:00"),
    ("Peak Morning", "10:00"),
    ("Lunch Peak", "12:00"),
    ("Afternoon", "15:00"),
    ("Evening", "18:00"),
    ("Night", "21:00"),
]

for time_label, time_str in times:
    r = requests.get(f"{base_url}?area=MG Road&area_type=commercial&time_of_day={time_str}")
    if r.status_code == 200:
        data = r.json()
        print(f"\n{time_label} ({time_str}):")
        print(f"  Availability: {data['availability']}")
        print(f"  Occupancy: {data['predicted_occupancy_percent']}%")
        print(f"  Confidence: {data['confidence']}")

# Comparison: Same time, different area types
print("\n" + "=" * 70)
print("[Comparison] MG Road at 12:00 - Different Area Types")
print("-" * 70)

area_types = ["commercial", "residential", "mixed"]

for atype in area_types:
    r = requests.get(f"{base_url}?area=MG Road&area_type={atype}&time_of_day=12:00")
    if r.status_code == 200:
        data = r.json()
        print(f"\n{atype.upper()}:")
        print(f"  Availability: {data['availability']}")
        print(f"  Occupancy: {data['predicted_occupancy_percent']}%")
        print(f"  Confidence: {data['confidence']}")

print("\n" + "=" * 70)
print("[OK] All tests completed!")
print("=" * 70)
print("\nTip: Visit http://localhost:8000/docs for interactive API testing")
print("\nScaling Notes:")
print("- Replace MOCK_HISTORICAL_OCCUPANCY with real time-series database")
print("- Add ML model (RandomForest, LSTM) for better predictions")
print("- Integrate real-time sensor data from parking systems")
print("- Add weather, events, and day-of-week features")

