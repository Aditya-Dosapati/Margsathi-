# Parking Predictor - cURL Examples

Quick reference for testing the parking availability predictor endpoint.

## Base URL
```
http://localhost:8000/api/parking/predict
```

## Example 1: MG Road - Commercial - Peak Hours
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=10:00"
```

## Example 2: BTM Layout - Residential - Evening
```bash
curl "http://localhost:8000/api/parking/predict?area=BTM%20Layout&area_type=residential&time_of_day=19:00"
```

## Example 3: MG Road - Mixed Area - Afternoon
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=mixed&time_of_day=15:00"
```

## Example 4: Late Night (High Availability Expected)
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=23:00"
```

## Example 5: Early Morning
```bash
curl "http://localhost:8000/api/parking/predict?area=BTM%20Layout&area_type=commercial&time_of_day=08:00"
```

## Example 6: Current Time (No time specified)
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial"
```

## Example 7: Lunch Peak (Low Availability Expected)
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=12:30"
```

## Example 8: Evening Rush Hour
```bash
curl "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=18:00"
```

## PowerShell Examples

### Example 1: Basic Request
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=10:00" -Method GET
```

### Example 2: Pretty Print JSON
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=10:00"
$response | ConvertTo-Json -Depth 10
```

### Example 3: Extract Specific Fields
```powershell
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/parking/predict?area=MG%20Road&area_type=commercial&time_of_day=10:00"
Write-Host "Availability: $($response.availability)"
Write-Host "Confidence: $($response.confidence)"
Write-Host "Occupancy: $($response.predicted_occupancy_percent)%"
```

## Python Examples

### Example 1: Basic Request
```python
import requests

response = requests.get(
    "http://localhost:8000/api/parking/predict",
    params={
        "area": "MG Road",
        "area_type": "commercial",
        "time_of_day": "10:00"
    }
)
print(response.json())
```

### Example 2: Multiple Areas
```python
import requests

areas = ["MG Road", "BTM Layout", "Koramangala"]
for area in areas:
    response = requests.get(
        "http://localhost:8000/api/parking/predict",
        params={"area": area, "area_type": "commercial", "time_of_day": "12:00"}
    )
    data = response.json()
    print(f"{area}: {data['availability']} ({data['predicted_occupancy_percent']}% occupied)")
```

## Expected Response Format

```json
{
  "area": "MG Road",
  "availability": "Low",
  "confidence": 0.95,
  "predicted_occupancy_percent": 95.0,
  "time_of_day": "10:00",
  "area_type": "commercial",
  "factors": {
    "base_occupancy": 85.0,
    "area_type_adjustment": 5.0,
    "time_adjustment": 5.0
  }
}
```

## Availability Levels

- **High**: < 50% occupancy (plenty of parking available)
- **Medium**: 50-80% occupancy (some parking available)
- **Low**: ≥ 80% occupancy (limited parking available)

## Area Types

- `commercial` - Business districts (peak during business hours)
- `residential` - Residential areas (peak in evenings)
- `mixed` - Mixed-use areas (balanced pattern)

## Testing Tips

1. **Peak Hours** (9-12, 17-19): Expect Low availability in commercial areas
2. **Off-Peak** (20-6): Expect High availability
3. **Residential Areas**: Higher occupancy in evenings (17-21)
4. **Commercial Areas**: Higher occupancy during business hours (10-15)

