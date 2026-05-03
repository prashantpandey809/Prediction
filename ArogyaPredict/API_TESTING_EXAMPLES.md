# API Testing Examples - ArogyaPredict

Complete examples of curl commands to test the ArogyaPredict REST API.

## Prerequisites

Before running these examples:
1. Start the API server: `python app/app.py`
2. API will be available at: `http://localhost:5000`

---

## 1. Health Check

Test if the API is running and ready to serve requests.

### Request
```bash
curl -X GET http://localhost:5000/health
```

### Response (Success - 200)
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00.123456",
    "model_loaded": true,
    "endpoints": ["/health", "/predict", "/recommend"]
}
```

---

## 2. Patient Count Prediction

### 2.1 Basic Prediction

Predict patient count with minimal required fields.

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65,
    "aqi": 150
  }'
```

#### Response (Success - 200)
```json
{
    "status": "success",
    "prediction": {
        "predicted_patient_count": 8.45,
        "rounded_count": 8,
        "confidence_range": {
            "lower": 6.45,
            "upper": 10.45
        }
    },
    "input": {
        "temperature": 28.5,
        "humidity": 65,
        "aqi": 150,
        "disease_type": "Heart Disease",
        "hospital_area": "General Ward"
    },
    "timestamp": "2024-01-15T10:30:00.123456"
}
```

---

### 2.2 Prediction with All Fields

Include optional disease_type and hospital_area for more targeted predictions.

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 32.0,
    "humidity": 78,
    "aqi": 200,
    "disease_type": "Respiratory Infection",
    "hospital_area": "Emergency"
  }'
```

#### Response
```json
{
    "status": "success",
    "prediction": {
        "predicted_patient_count": 15.32,
        "rounded_count": 15,
        "confidence_range": {
            "lower": 13.32,
            "upper": 17.32
        }
    },
    "input": {
        "temperature": 32.0,
        "humidity": 78,
        "aqi": 200,
        "disease_type": "Respiratory Infection",
        "hospital_area": "Emergency"
    },
    "timestamp": "2024-01-15T10:35:00.654321"
}
```

---

### 2.3 Extreme Environmental Conditions

Test prediction with severe environmental stress.

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 40.0,
    "humidity": 90,
    "aqi": 350,
    "disease_type": "Hypertension",
    "hospital_area": "ICU"
  }'
```

#### Response
```json
{
    "status": "success",
    "prediction": {
        "predicted_patient_count": 22.15,
        "rounded_count": 22,
        "confidence_range": {
            "lower": 20.15,
            "upper": 24.15
        }
    }
}
```

---

### 2.4 Low Environmental Stress

Test prediction with favorable environmental conditions.

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 20.0,
    "humidity": 45,
    "aqi": 50,
    "disease_type": "Diabetes",
    "hospital_area": "OPD"
  }'
```

#### Response
```json
{
    "status": "success",
    "prediction": {
        "predicted_patient_count": 3.21,
        "rounded_count": 3,
        "confidence_range": {
            "lower": 1.21,
            "upper": 5.21
        }
    }
}
```

---

## 3. Error Handling Examples

### 3.1 Missing Required Field

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65
  }'
```

#### Response (Error - 400)
```json
{
    "error": "Missing required field: 'aqi'",
    "status": "error"
}
```

---

### 3.2 Invalid Data Type

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": "not_a_number",
    "humidity": 65,
    "aqi": 150
  }'
```

#### Response (Error - 400)
```json
{
    "error": "Temperature, humidity, and AQI must be numeric values",
    "status": "error"
}
```

---

### 3.3 Invalid Humidity Range

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 150,
    "aqi": 150
  }'
```

#### Response (Error - 400)
```json
{
    "error": "Humidity must be between 0 and 100",
    "status": "error"
}
```

---

### 3.4 Invalid Temperature Range

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 100,
    "humidity": 65,
    "aqi": 150
  }'
```

#### Response (Error - 400)
```json
{
    "error": "Temperature must be between -50 and 60°C",
    "status": "error"
}
```

---

### 3.5 Non-existent Endpoint

#### Request
```bash
curl -X GET http://localhost:5000/invalid
```

#### Response (Error - 404)
```json
{
    "error": "Endpoint not found",
    "status": "error",
    "available_endpoints": ["/health", "/predict", "/recommend"]
}
```

---

### 3.6 Wrong HTTP Method

#### Request
```bash
curl -X GET http://localhost:5000/predict
```

#### Response (Error - 405)
```json
{
    "error": "Method not allowed",
    "status": "error"
}
```

---

## 4. Medicine Recommendations

### 4.1 Low Patient Count - Decrease Stock

Recommend reducing stock for low patient count.

#### Request
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 2,
    "disease_type": "Diabetes",
    "current_stock": 100
  }'
```

#### Response (Success - 200)
```json
{
    "status": "success",
    "input": {
        "predicted_patient_count": 2,
        "disease_type": "Diabetes",
        "current_stock": 100
    },
    "recommendations": [
        {
            "medicine": "Insulin",
            "current_stock": 100,
            "recommended_quantity": 72,
            "action": "Decrease stock",
            "expiry_warning": "Check expiry within 7 days",
            "criticality": "NORMAL"
        },
        {
            "medicine": "Metformin",
            "current_stock": 100,
            "recommended_quantity": 54,
            "action": "Decrease stock",
            "expiry_warning": "Check expiry within 90 days",
            "criticality": "NORMAL"
        },
        {
            "medicine": "Glipizide",
            "current_stock": 100,
            "recommended_quantity": 36,
            "action": "Decrease stock",
            "expiry_warning": "Check expiry within 90 days",
            "criticality": "NORMAL"
        }
    ],
    "summary": {
        "total_medicines": 3,
        "critical_count": 0,
        "high_count": 0
    },
    "timestamp": "2024-01-15T10:40:00.123456"
}
```

---

### 4.2 High Patient Count - Increase Stock

Recommend increasing stock for high patient count.

#### Request
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 20,
    "disease_type": "Heart Disease",
    "current_stock": 100
  }'
```

#### Response
```json
{
    "status": "success",
    "input": {
        "predicted_patient_count": 20,
        "disease_type": "Heart Disease",
        "current_stock": 100
    },
    "recommendations": [
        {
            "medicine": "Aspirin",
            "current_stock": 100,
            "recommended_quantity": 240,
            "action": "Increase stock",
            "expiry_warning": "Check expiry within 30 days",
            "criticality": "NORMAL"
        },
        {
            "medicine": "Atorvastatin",
            "current_stock": 100,
            "recommended_quantity": 120,
            "action": "Increase stock",
            "expiry_warning": "Check expiry within 60 days",
            "criticality": "NORMAL"
        },
        {
            "medicine": "Lisinopril",
            "current_stock": 100,
            "recommended_quantity": 120,
            "action": "Increase stock",
            "expiry_warning": "Check expiry within 60 days",
            "criticality": "NORMAL"
        }
    ],
    "summary": {
        "total_medicines": 3,
        "critical_count": 0,
        "high_count": 0
    },
    "timestamp": "2024-01-15T10:45:00.654321"
}
```

---

### 4.3 Critical Stock Level

Alert when stock is critically low.

#### Request
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 15,
    "disease_type": "Respiratory Infection",
    "current_stock": 15
  }'
```

#### Response
```json
{
    "status": "success",
    "input": {
        "predicted_patient_count": 15,
        "disease_type": "Respiratory Infection",
        "current_stock": 15
    },
    "recommendations": [
        {
            "medicine": "Amoxicillin",
            "current_stock": 15,
            "recommended_quantity": 342,
            "action": "URGENT: Order immediately",
            "expiry_warning": "Prioritize stock with latest expiry dates",
            "criticality": "CRITICAL"
        },
        {
            "medicine": "Salbutamol",
            "current_stock": 15,
            "recommended_quantity": 228,
            "action": "URGENT: Order immediately",
            "expiry_warning": "Prioritize stock with latest expiry dates",
            "criticality": "CRITICAL"
        },
        {
            "medicine": "Omeprazole",
            "current_stock": 15,
            "recommended_quantity": 285,
            "action": "URGENT: Order immediately",
            "expiry_warning": "Prioritize stock with latest expiry dates",
            "criticality": "CRITICAL"
        }
    ],
    "summary": {
        "total_medicines": 3,
        "critical_count": 3,
        "high_count": 0
    },
    "timestamp": "2024-01-15T10:50:00.987654"
}
```

---

### 4.4 Low Stock Level (Not Critical)

Alert when stock is low but not critical.

#### Request
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 12,
    "disease_type": "Hypertension",
    "current_stock": 45
  }'
```

#### Response
```json
{
    "status": "success",
    "input": {
        "predicted_patient_count": 12,
        "disease_type": "Hypertension",
        "current_stock": 45
    },
    "recommendations": [
        {
            "medicine": "Amlodipine",
            "current_stock": 45,
            "recommended_quantity": 168,
            "action": "Order soon",
            "expiry_warning": "Check expiry within 90 days",
            "criticality": "HIGH"
        },
        {
            "medicine": "Atenolol",
            "current_stock": 45,
            "recommended_quantity": 144,
            "action": "Order soon",
            "expiry_warning": "Check expiry within 90 days",
            "criticality": "HIGH"
        }
    ],
    "summary": {
        "total_medicines": 2,
        "critical_count": 0,
        "high_count": 2
    },
    "timestamp": "2024-01-15T10:55:00.321654"
}
```

---

## 5. Batch Testing

### Run Multiple Predictions

```bash
# Create a loop for batch predictions
for temp in 20 25 30 35 40; do
  echo "Testing with temperature: $temp"
  curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d "{\"temperature\": $temp, \"humidity\": 65, \"aqi\": 150}" \
    | python -m json.tool
  echo ""
done
```

---

## 6. Using Python Requests

If you prefer Python over curl:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Health Check
response = requests.get(f"{BASE_URL}/health")
print(json.dumps(response.json(), indent=2))

# Prediction
data = {
    "temperature": 28.5,
    "humidity": 65,
    "aqi": 150
}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(json.dumps(response.json(), indent=2))

# Recommendation
data = {
    "predicted_patient_count": 10,
    "disease_type": "Heart Disease",
    "current_stock": 100
}
response = requests.post(f"{BASE_URL}/recommend", json=data)
print(json.dumps(response.json(), indent=2))
```

---

## 7. Save Response to File

```bash
# Save prediction response to file
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65, "aqi": 150}' \
  > prediction_response.json

# Pretty print the response
cat prediction_response.json | python -m json.tool
```

---

## 8. Performance Testing

### Test Response Time

```bash
# Measure API response time
time curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65, "aqi": 150}'

# Using Apache Bench (if installed)
ab -n 100 -c 10 -p data.json -T application/json http://localhost:5000/predict
```

---

## 📋 Summary

| Endpoint | Method | Status | Example |
|----------|--------|--------|---------|
| /health | GET | 200 | Health check |
| /predict | POST | 200 | Patient prediction |
| /predict | POST | 400 | Invalid input |
| /predict | POST | 503 | Model not loaded |
| /recommend | POST | 200 | Get recommendations |
| /recommend | POST | 400 | Invalid input |
| /invalid | ANY | 404 | Not found |
| /predict | GET | 405 | Wrong method |

---

## 🚀 Next Steps

1. **Test all examples** above with the API running
2. **Modify parameters** to test different scenarios
3. **Integrate into your application** using the responses
4. **Monitor performance** and optimize as needed

---

**Happy Testing! 🎉**
