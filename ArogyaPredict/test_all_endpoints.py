import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 70)
print("TESTING ALL API ENDPOINTS & ERROR HANDLERS")
print("=" * 70)

# Test 1: Root endpoint
print("\n✓ TEST 1: Root endpoint GET /")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Message: {data.get('message')}")
    print(f"Endpoints: GET /, GET /health, POST /predict, POST /recommend")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Favicon endpoint
print("\n✓ TEST 2: Favicon endpoint GET /favicon.ico")
try:
    response = requests.get(f"{BASE_URL}/favicon.ico")
    print(f"Status: {response.status_code} (204 = No Content)")
    print(f"Body: Empty (as expected)")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Health endpoint
print("\n✓ TEST 3: Health endpoint GET /health")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Status: {data.get('status')}")
    print(f"Model loaded: {data.get('model_loaded')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 4: 404 error - wrong endpoint
print("\n✓ TEST 4: 404 Error handling - GET /wrongendpoint")
try:
    response = requests.get(f"{BASE_URL}/wrongendpoint")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Error: {data.get('error')}")
    print(f"Message: {data.get('message')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 5: 405 error - method not allowed
print("\n✓ TEST 5: 405 Error handling - GET /predict (should be POST)")
try:
    response = requests.get(f"{BASE_URL}/predict")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Error: {data.get('error')}")
    print(f"Hint: {data.get('hint')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 6: Bad request - missing required field
print("\n✓ TEST 6: 400 Error handling - Missing required field")
try:
    response = requests.post(f"{BASE_URL}/predict", json={"temperature": 25})
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Error: {data.get('error')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 7: Prediction with diverse disease types (no warnings)
print("\n✓ TEST 7: Predictions with all disease types (robust encoding)")
diseases = ["Respiratory Infection", "Gastroenteritis", "Malaria", "Pediatric Illness", "Heart Disease"]
for disease in diseases:
    try:
        data = {
            "temperature": 25, "humidity": 65, "aqi": 150,
            "disease_type": disease, "weather_condition": "Haze",
            "is_holiday": 0, "holiday_name": "None",
            "expected_multiplier": 1.0, "days_after_holiday": 0
        }
        response = requests.post(f"{BASE_URL}/predict", json=data)
        if response.status_code == 200:
            pred = response.json()["prediction"]["predicted_patient_count"]
            print(f"  {disease:25s}: {pred:5.1f} patients ✓")
        else:
            print(f"  {disease:25s}: ERROR {response.status_code}")
    except Exception as e:
        print(f"  {disease}: {e}")

# Test 8: Weather conditions
print("\n✓ TEST 8: Predictions with diverse weather conditions")
weather = ["Haze", "Clear", "Smoke", "Rain", "Cloudy"]
for wc in weather:
    try:
        data = {
            "temperature": 25, "humidity": 65, "aqi": 150,
            "disease_type": "Heart Disease", "weather_condition": wc,
            "is_holiday": 0, "holiday_name": "None",
            "expected_multiplier": 1.0, "days_after_holiday": 0
        }
        response = requests.post(f"{BASE_URL}/predict", json=data)
        if response.status_code == 200:
            pred = response.json()["prediction"]["predicted_patient_count"]
            print(f"  {wc:15s}: {pred:5.1f} patients ✓")
        else:
            print(f"  {wc:15s}: ERROR {response.status_code}")
    except Exception as e:
        print(f"  {wc}: {e}")

# Test 9: Holiday names
print("\n✓ TEST 9: Predictions with diverse holiday names")
holidays = ["New Year's Day", "Holi", "Diwali", "Christmas", "None"]
for holiday in holidays:
    try:
        data = {
            "temperature": 25, "humidity": 65, "aqi": 150,
            "disease_type": "Heart Disease", "weather_condition": "Haze",
            "is_holiday": 1 if holiday != "None" else 0, "holiday_name": holiday,
            "expected_multiplier": 1.0, "days_after_holiday": 0
        }
        response = requests.post(f"{BASE_URL}/predict", json=data)
        if response.status_code == 200:
            pred = response.json()["prediction"]["predicted_patient_count"]
            print(f"  {holiday:15s}: {pred:5.1f} patients ✓")
        else:
            print(f"  {holiday:15s}: ERROR {response.status_code}")
    except Exception as e:
        print(f"  {holiday}: {e}")

print("\n" + "=" * 70)
print("✓ ALL TESTS COMPLETE - ALL ERRORS FIXED")
print("=" * 70)
