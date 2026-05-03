# 🏥 ArogyaPredict Dashboard - User Guide

## Overview

The ArogyaPredict Dashboard is a modern, user-friendly web interface for hospital patient inflow prediction and medicine stock management. It provides real-time analytics, comprehensive medicine database, and intelligent stock recommendations.

## Features

### 📊 Key Features

1. **Today's Overview Dashboard**
   - Real-time predicted patient count for today
   - Confidence range for predictions
   - Monthly estimates with average daily calculations
   - Critical medicine items alert system
   - Expiry tracking for medicines

2. **Prediction Engine** 🔮
   - Interactive form for making predictions
   - Input parameters:
     - Temperature (°C)
     - Humidity (%)
     - Air Quality Index (AQI)
     - Disease Type selection
     - Weather conditions
     - Holiday information
   - Instant prediction results with confidence ranges

3. **Comprehensive Medicine Database** 💊
   - **50+ medicines** across 10 disease categories
   - Search and filter functionality
   - Detailed medicine information:
     - Dosage specifications
     - Medicine form (Tablet, Injection, etc.)
     - Base quantity
     - Expiry critical days
   - Disease categories covered:
     - ❤️ Heart Disease (6 medicines)
     - 🩺 Diabetes (7 medicines)
     - 🫁 Respiratory Infection (8 medicines)
     - 🏥 Hypertension (6 medicines)
     - 🔴 Cancer (5 medicines)
     - 🫘 Kidney Disease (5 medicines)
     - 🍽️ Gastroenteritis (6 medicines)
     - 🦴 Fractures (6 medicines)
     - 🧠 Stroke (5 medicines)
     - 📋 Other (5 medicines)

4. **Analytics & Charts** 📈
   - 30-day patient forecast visualization
   - Disease type distribution chart
   - Interactive, responsive charts

5. **Smart Recommendations** ⚕️
   - Context-aware medicine recommendations
   - Stock level recommendations based on predicted patient count
   - Criticality assessment:
     - 🔴 **CRITICAL**: Stock below 20 units
     - 🟠 **HIGH**: Stock below 50 units
     - 🟢 **NORMAL**: Stock above 50 units
   - Action recommendations:
     - URGENT: Order immediately
     - Order soon
     - Increase stock
     - Decrease stock
     - Maintain current stock

## How to Use

### 1. Starting the Application

```bash
cd ArogyaPredict
python -m app.app
```

The dashboard will be available at: `http://localhost:5000`

### 2. Making a Prediction

**Step 1:** Fill in the environmental data

- Enter temperature, humidity, and AQI values
- Select disease type
- Choose weather condition
- Indicate if it's a holiday

**Step 2:** Click "Predict Patient Count"

**Step 3:** View results

- Predicted patient count displayed prominently
- Confidence range shown
- Medicine recommendations automatically generated

### 3. Browsing Medicine Database

**Option A - View All:**
Simply scroll to the "Comprehensive Medicine Database" section to see all 50+ medicines

**Option B - Filter by Disease:**

1. Select disease type from dropdown
2. Medicines automatically filtered

**Option C - Search:**

1. Use the search box
2. Search by medicine name or disease
3. Results filter in real-time

### 4. Getting Stock Recommendations

**Step 1:** Enter prediction parameters:

- Predicted patient count (e.g., 15)
- Disease type
- Current stock level

**Step 2:** Click "Get Recommendations"

**Step 3:** Review recommendations:

- Each medicine gets a criticality level
- Recommended quantity calculated
- Action items provided
- Expiry warnings included

## Medicine Database Structure

Each medicine contains:

```json
{
  "name": "Medicine Name",
  "base_qty": 200, // Base quantity in units
  "expiry_critical_days": 30, // Days before expiry alert
  "dosage": "100mg", // Standard dosage
  "form": "Tablet" // Form (Tablet, Injection, etc.)
}
```

### Disease Categories & Medicine Count

| Disease         | Medicines | Examples                                                                                               |
| --------------- | --------- | ------------------------------------------------------------------------------------------------------ |
| Heart Disease   | 6         | Aspirin, Atorvastatin, Lisinopril, Metoprolol, Nitroglycerin, Clopidogrel                              |
| Diabetes        | 7         | Insulin, Metformin, Glipizide, Sitagliptin, Pioglitazone, Acarbose, Exenatide                          |
| Respiratory     | 8         | Amoxicillin, Azithromycin, Salbutamol, Omeprazole, Levofloxacin, Fluticasone, Montelukast, Paracetamol |
| Hypertension    | 6         | Amlodipine, Atenolol, Losartan, Enalapril, Hydrochlorothiazide, Valsartan                              |
| Cancer          | 5         | Cisplatin, Methotrexate, Doxorubicin, Paclitaxel, Tamoxifen                                            |
| Kidney Disease  | 5         | Furosemide, Potassium, Calcium Carbonate, Phosphate Binder, Erythropoietin                             |
| Gastroenteritis | 6         | Metoclopramide, Ondansetron, Loperamide, Ciprofloxacin, Electrolyte, Bismuth                           |
| Fractures       | 6         | Ibuprofen, Paracetamol, Tramadol, Calcium, Vitamin D, Tetanus                                          |
| Stroke          | 5         | Aspirin, Ticlopidine, Alteplase, Atorvastatin, Lisinopril                                              |
| Other           | 5         | Antihistamine, Iodine, Bandages, Saline, Wipes                                                         |

## API Endpoints

### Dashboard Endpoints

- **GET `/`** - Root (auto-detects browser and serves dashboard)
- **GET `/dashboard`** - Interactive dashboard page
- **GET `/health`** - System health status

### Prediction Endpoints

- **POST `/predict`** - Get patient count prediction
- **GET `/api/predictions/weekly`** - Weekly prediction summary

### Medicine & Recommendation Endpoints

- **GET `/api/medicines`** - Get complete medicine database
- **GET `/api/medicines?disease_type=Diabetes`** - Filter by disease
- **POST `/recommend`** - Get medicine stock recommendations

## Example API Calls

### Predict Patient Count

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65,
    "aqi": 150,
    "disease_type": "Heart Disease",
    "weather_condition": "Haze",
    "is_holiday": 0,
    "holiday_name": "None",
    "expected_multiplier": 1.0,
    "days_after_holiday": 0
  }'
```

### Get Medicine Recommendations

```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 15,
    "disease_type": "Heart Disease",
    "current_stock": 100
  }'
```

### Get All Medicines

```bash
curl http://localhost:5000/api/medicines
```

### Filter Medicines by Disease

```bash
curl http://localhost:5000/api/medicines?disease_type=Diabetes
```

## Understanding Recommendations

### Stock Level Colors

- 🔴 **CRITICAL** (< 20 units): Needs immediate attention
- 🟠 **HIGH** (20-50 units): Should order soon
- 🟢 **NORMAL** (> 50 units): Sufficient stock

### Action Items

| Action                    | Condition                        | Recommendation   |
| ------------------------- | -------------------------------- | ---------------- |
| URGENT: Order immediately | Stock < 20                       | Increase by 50%+ |
| Order soon                | 20 ≤ Stock < 50                  | Increase by 20%  |
| Increase stock            | Stock ≥ 50 but patients > 10     | Increase by 20%  |
| Decrease stock            | Stock ≥ 50 and patients < 3      | Decrease by 10%  |
| Maintain current          | Stock ≥ 50 and 3 ≤ patients ≤ 10 | Keep as is       |

## Key Metrics Explained

### Predicted Patient Count

- Machine learning model prediction based on:
  - Environmental data (temperature, humidity, AQI)
  - Disease type
  - Weather conditions
  - Holiday status

### Confidence Range

- Lower bound: Predicted - 2 patients
- Upper bound: Predicted + 2 patients
- Helps in planning minimum/maximum stock

### Monthly Estimate

- Based on 25 working days
- Average daily × 25 = Monthly estimate

## Tips & Best Practices

### 1. Accurate Predictions

- Use current/today's environmental data for best results
- Update weather and AQI from local sources
- Consider holiday impacts on patient flow

### 2. Medicine Management

- Order medicines before reaching CRITICAL levels
- Follow expiry date recommendations
- Keep buffer stock for high-volume diseases
- Review and update current stock regularly

### 3. Planning

- Use weekly predictions for bulk ordering
- Monitor disease trends through the charts
- Maintain diverse medicine inventory
- Track seasonal patterns

## Troubleshooting

### Dashboard Not Loading?

- Check if Flask server is running
- Ensure no port conflicts on 5000
- Clear browser cache and reload

### Predictions Seem Off?

- Verify environmental data accuracy
- Check if model is properly trained
- Review past predictions for patterns

### Medicine Recommendations Not Updating?

- Refresh the page
- Ensure current stock value is correct
- Verify disease type is selected

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Database**: In-memory (expandable to SQL)
- **Architecture**: REST API with SPA Dashboard

## Support & Documentation

For more information, see:

- [README.md](../README.md) - Project overview
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System design
- [API_TESTING_EXAMPLES.md](../API_TESTING_EXAMPLES.md) - API examples

---

**Version**: 1.0  
**Last Updated**: April 2024  
**Status**: Production Ready ✅
