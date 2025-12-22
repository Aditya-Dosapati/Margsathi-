"""
Test examples for the translation endpoint.
Run this while your FastAPI server is running on http://localhost:8000
"""
import requests
import json
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")

BASE_URL = "http://localhost:8000/api/translation/simple"

print("=" * 80)
print("TRANSLATION API - Test Examples")
print("=" * 80)

# Example 1: Basic translation - English to Hindi
print("\n" + "=" * 80)
print("Example 1: English to Hindi - Basic Text")
print("=" * 80)
payload_1 = {
    "text": "Hello MARGSATHI",
    "target_lang": "hi"
}
r1 = requests.post(BASE_URL, json=payload_1)
if r1.status_code == 200:
    data = r1.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_1, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
    print(f"\n[INFO] Original: {data['original_text']}")
    print(f"[INFO] Translated: {data['translated_text']}")
else:
    print(f"[ERROR] Error: {r1.status_code} - {r1.text}")

# Example 2: Sign translation - Parking sign
print("\n" + "=" * 80)
print("Example 2: Parking Sign Translation - English to Hindi")
print("=" * 80)
payload_2 = {
    "text": "Parking Available",
    "target_lang": "hi"
}
r2 = requests.post(BASE_URL, json=payload_2)
if r2.status_code == 200:
    data = r2.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_2, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r2.status_code} - {r2.text}")

# Example 3: Direction sign
print("\n" + "=" * 80)
print("Example 3: Direction Sign - English to Tamil")
print("=" * 80)
payload_3 = {
    "text": "Turn Left for MG Road",
    "target_lang": "ta"
}
r3 = requests.post(BASE_URL, json=payload_3)
if r3.status_code == 200:
    data = r3.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_3, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r3.status_code} - {r3.text}")

# Example 4: Warning sign
print("\n" + "=" * 80)
print("Example 4: Warning Sign - English to Bengali")
print("=" * 80)
payload_4 = {
    "text": "No Parking",
    "target_lang": "bn"
}
r4 = requests.post(BASE_URL, json=payload_4)
if r4.status_code == 200:
    data = r4.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_4, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r4.status_code} - {r4.text}")

# Example 5: Information sign
print("\n" + "=" * 80)
print("Example 5: Information Sign - English to Telugu")
print("=" * 80)
payload_5 = {
    "text": "Bus Stop Ahead",
    "target_lang": "te"
}
r5 = requests.post(BASE_URL, json=payload_5)
if r5.status_code == 200:
    data = r5.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_5, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r5.status_code} - {r5.text}")

# Example 6: Route instruction
print("\n" + "=" * 80)
print("Example 6: Route Instruction - English to Marathi")
print("=" * 80)
payload_6 = {
    "text": "Take the next right turn",
    "target_lang": "mr"
}
r6 = requests.post(BASE_URL, json=payload_6)
if r6.status_code == 200:
    data = r6.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_6, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r6.status_code} - {r6.text}")

# Example 7: Event notification
print("\n" + "=" * 80)
print("Example 7: Event Notification - English to Kannada")
print("=" * 80)
payload_7 = {
    "text": "Road closed due to event",
    "target_lang": "kn"
}
r7 = requests.post(BASE_URL, json=payload_7)
if r7.status_code == 200:
    data = r7.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_7, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r7.status_code} - {r7.text}")

# Example 8: Multiple languages comparison
print("\n" + "=" * 80)
print("Example 8: Same Text - Multiple Languages Comparison")
print("=" * 80)

text = "Parking Available"
languages = [
    ("Hindi", "hi"),
    ("Tamil", "ta"),
    ("Telugu", "te"),
    ("Bengali", "bn"),
    ("Marathi", "mr"),
    ("Kannada", "kn"),
    ("Malayalam", "ml"),
    ("Gujarati", "gu"),
]

print(f"\nOriginal Text: '{text}'")
print("\nTranslations:")
print("-" * 80)

for lang_name, lang_code in languages:
    payload = {"text": text, "target_lang": lang_code}
    r = requests.post(BASE_URL, json=payload)
    if r.status_code == 200:
        data = r.json()
        print(f"{lang_name:12} ({lang_code}): {data['translated_text']}")
    else:
        print(f"{lang_name:12} ({lang_code}): [ERROR]")

# Example 9: Long text (sign with multiple lines)
print("\n" + "=" * 80)
print("Example 9: Long Sign Text - English to Hindi")
print("=" * 80)
payload_9 = {
    "text": "Welcome to MARGSATHI Mobility Platform. Find parking, plan routes, and stay informed about events.",
    "target_lang": "hi"
}
r9 = requests.post(BASE_URL, json=payload_9)
if r9.status_code == 200:
    data = r9.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_9, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
else:
    print(f"[ERROR] Error: {r9.status_code} - {r9.text}")

# Example 10: With source language specified
print("\n" + "=" * 80)
print("Example 10: With Source Language - English to Hindi")
print("=" * 80)
payload_10 = {
    "text": "No Entry",
    "target_lang": "hi",
    "source_lang": "en"
}
r10 = requests.post(BASE_URL, json=payload_10)
if r10.status_code == 200:
    data = r10.json()
    print(f"\n[OK] Request:")
    print(json.dumps(payload_10, indent=2))
    print(f"\n[OK] Response:")
    print(json.dumps(data, indent=2))
    print(f"\n[INFO] Source Language: {data['source_lang']}")
    print(f"[INFO] Target Language: {data['target_lang']}")
else:
    print(f"[ERROR] Error: {r10.status_code} - {r10.text}")

print("\n" + "=" * 80)
print("[OK] All examples completed!")
print("=" * 80)
print("\n[INFO] Tip: Visit http://localhost:8000/docs for interactive API testing")
print("\n[INFO] Note: This is a mock translation service. In production, replace")
print("       with a real translation API (Google Translate, Azure Translator, etc.)")

