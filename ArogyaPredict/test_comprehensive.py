"""Comprehensive API Testing Script"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Heart Disease with high AQI and cold weather
print("=== TEST 1: Heart Disease with Extreme Cold ===")
data1 = {
    "temperature": -15,
    "humidity": 80,
    "aqi": 300,
    "disease_type": "Heart Disease",
    "weather_condition": "Smoke",
    "is_holiday": 0,
    "holiday_name": "None",
    "expected_multiplier": 1.4,
    "days_after_holiday": 0
}

response1 = requests.post(f"{BASE_URL}/predict", json=data1)
result1 = response1.json()
print(f"Status: {result1['status']}")
print(f"Prediction: {result1['prediction']['predicted_patient_count']} patients")
print(f"Confidence: {result1['prediction']['confidence_range']}\n")

# Test 2: Gastroenteritis during rainy season
print("=== TEST 2: Gastroenteritis During Rainy Season ===")
data2 = {
    "temperature": 28,
    "humidity": 95,
    "aqi": 120,
    "disease_type": "Gastroenteritis",
    "weather_condition": "Rain",
    "is_holiday": 0,
    "holiday_name": "None",
    "expected_multiplier": 1.3,
    "days_after_holiday": 0
}

response2 = requests.post(f"{BASE_URL}/predict", json=data2)
result2 = response2.json()
print(f"Status: {result2['status']}")
print(f"Prediction: {result2['prediction']['predicted_patient_count']} patients")
print(f"Confidence: {result2['prediction']['confidence_range']}\n")

# Test 3: Malaria with minimal factors
print("=== TEST 3: Malaria - Baseline Conditions ===")
data3 = {
    "temperature": 30,
    "humidity": 60,
    "aqi": 80,
    "disease_type": "Malaria",
    "weather_condition": "Clear",
    "is_holiday": 0,
    "holiday_name": "None",
    "expected_multiplier": 1.0,
    "days_after_holiday": 0
}

response3 = requests.post(f"{BASE_URL}/predict", json=data3)
result3 = response3.json()
print(f"Status: {result3['status']}")
print(f"Prediction: {result3['prediction']['predicted_patient_count']} patients")
print(f"Confidence: {result3['prediction']['confidence_range']}\n")

# Test 4: Pediatric Illness with holiday boost
print("=== TEST 4: Pediatric Illness During Holiday Season ===")
data4 = {
    "temperature": 22,
    "humidity": 70,
    "aqi": 110,
    "disease_type": "Pediatric Illness",
    "weather_condition": "Haze",
    "is_holiday": 1,
    "holiday_name": "Holi",
    "expected_multiplier": 1.2,
    "days_after_holiday": 1
}

response4 = requests.post(f"{BASE_URL}/predict", json=data4)
result4 = response4.json()
print(f"Status: {result4['status']}")
print(f"Prediction: {result4['prediction']['predicted_patient_count']} patients")
print(f"Confidence: {result4['prediction']['confidence_range']}\n")

# Test 5: Health endpoint
print("=== TEST 5: Health Check ===")
health = requests.get(f"{BASE_URL}/health")
print(json.dumps(health.json(), indent=2))
