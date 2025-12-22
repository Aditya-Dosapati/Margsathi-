# Translation API - Test Examples

Quick reference for testing the translation endpoint, especially for sign translations.

## Base URL
```
POST http://localhost:8000/api/translation/simple
```

## Supported Languages

- `en` - English
- `hi` - Hindi
- `bn` - Bengali
- `ta` - Tamil
- `te` - Telugu
- `mr` - Marathi
- `kn` - Kannada
- `ml` - Malayalam
- `gu` - Gujarati

## Example 1: Basic Translation (English to Hindi)

**Request:**
```json
{
  "text": "Hello MARGSATHI",
  "target_lang": "hi"
}
```

**Response:**
```json
{
  "original_text": "Hello MARGSATHI",
  "translated_text": "[HI] Hello MARGSATHI",
  "source_lang": "en",
  "target_lang": "hi",
  "is_mock": true
}
```

## Example 2: Parking Sign Translation

**Request:**
```json
{
  "text": "Parking Available",
  "target_lang": "hi"
}
```

**PowerShell:**
```powershell
$body = @{
    text = "Parking Available"
    target_lang = "hi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/translation/simple" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## Example 3: Direction Sign (English to Tamil)

**Request:**
```json
{
  "text": "Turn Left for MG Road",
  "target_lang": "ta"
}
```

## Example 4: Warning Sign (English to Bengali)

**Request:**
```json
{
  "text": "No Parking",
  "target_lang": "bn"
}
```

## Example 5: Information Sign (English to Telugu)

**Request:**
```json
{
  "text": "Bus Stop Ahead",
  "target_lang": "te"
}
```

## Example 6: Route Instruction (English to Marathi)

**Request:**
```json
{
  "text": "Take the next right turn",
  "target_lang": "mr"
}
```

## Example 7: Event Notification (English to Kannada)

**Request:**
```json
{
  "text": "Road closed due to event",
  "target_lang": "kn"
}
```

## Example 8: With Source Language Specified

**Request:**
```json
{
  "text": "No Entry",
  "target_lang": "hi",
  "source_lang": "en"
}
```

## Common Sign Translations

### Parking Signs
```json
{"text": "Parking Available", "target_lang": "hi"}
{"text": "No Parking", "target_lang": "hi"}
{"text": "Parking Full", "target_lang": "hi"}
{"text": "Reserved Parking", "target_lang": "hi"}
```

### Direction Signs
```json
{"text": "Turn Left", "target_lang": "ta"}
{"text": "Turn Right", "target_lang": "ta"}
{"text": "Go Straight", "target_lang": "ta"}
{"text": "U-Turn Allowed", "target_lang": "ta"}
```

### Warning Signs
```json
{"text": "Road Closed", "target_lang": "bn"}
{"text": "Construction Ahead", "target_lang": "bn"}
{"text": "Slow Down", "target_lang": "bn"}
{"text": "No Entry", "target_lang": "bn"}
```

### Information Signs
```json
{"text": "Bus Stop", "target_lang": "te"}
{"text": "Metro Station", "target_lang": "te"}
{"text": "Hospital Ahead", "target_lang": "te"}
{"text": "Restaurant Zone", "target_lang": "te"}
```

## PowerShell Examples

### Basic Translation
```powershell
$body = @{
    text = "Parking Available"
    target_lang = "hi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/translation/simple" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Multiple Languages
```powershell
$text = "Parking Available"
$languages = @("hi", "ta", "te", "bn", "mr", "kn", "ml", "gu")

foreach ($lang in $languages) {
    $body = @{
        text = $text
        target_lang = $lang
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/translation/simple" `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "$lang : $($response.translated_text)"
}
```

## Python Examples

### Basic Translation
```python
import requests

response = requests.post(
    "http://localhost:8000/api/translation/simple",
    json={
        "text": "Parking Available",
        "target_lang": "hi"
    }
)
print(response.json())
```

### Translate Multiple Signs
```python
import requests

signs = [
    "Parking Available",
    "No Parking",
    "Turn Left",
    "Road Closed",
    "Bus Stop Ahead"
]

for sign in signs:
    response = requests.post(
        "http://localhost:8000/api/translation/simple",
        json={"text": sign, "target_lang": "hi"}
    )
    data = response.json()
    print(f"{sign} → {data['translated_text']}")
```

## cURL Examples

### Basic Translation
```bash
curl -X POST "http://localhost:8000/api/translation/simple" \
  -H "Content-Type: application/json" \
  -d '{"text": "Parking Available", "target_lang": "hi"}'
```

### With Source Language
```bash
curl -X POST "http://localhost:8000/api/translation/simple" \
  -H "Content-Type: application/json" \
  -d '{"text": "No Entry", "target_lang": "hi", "source_lang": "en"}'
```

## Expected Response Format

```json
{
  "original_text": "Parking Available",
  "translated_text": "[HI] Parking Available",
  "source_lang": "en",
  "target_lang": "hi",
  "is_mock": true
}
```

## Note

⚠️ **This is a mock translation service** for hackathon/demo purposes. It simply adds a language marker prefix to the text. 

For production, replace with:
- Google Cloud Translation API
- Azure Translator
- AWS Translate
- DeepL API
- Or any other translation service

## Testing Tips

1. **Use Swagger UI**: Visit `http://localhost:8000/docs` for interactive testing
2. **Test all languages**: Try translating the same text to all supported languages
3. **Test sign text**: Use common sign phrases like "Parking Available", "No Entry", etc.
4. **Test long text**: Try longer sentences to see how the API handles them

