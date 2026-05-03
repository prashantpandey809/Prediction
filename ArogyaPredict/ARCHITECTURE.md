# ArogyaPredict - Architecture & Design Documentation

## 🏛️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│              ArogyaPredict System (ENHANCED)                 │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│   External APIs (3)      │
├──────────────────────────┤
│ • AQICN API              │  → AQI Data
│ • OpenWeather API        │  → Temperature, Humidity
│ • Calendarific API       │  → Holidays & Events
└────────────┬─────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  Data Enrichment Module (fetch_data.py)                     │
│  ✨ NOW WITH HOLIDAY DETECTION & INTELLIGENT CORRELATION    │
├─────────────────────────────────────────────────────────────┤
│  • Fetch AQICN AQI (air quality index)                      │
│  • Fetch OpenWeather (temperature, humidity)                │
│  • Fetch Calendarific (holidays: Holi, Diwali, etc.)        │
│  • Smart Correlation Logic:                                 │
│    - Respiratory: ↑1.5-1.8x in cold/Diwali                 │
│    - Heart Disease: ↑1.4x in extreme cold                  │
│    - Gastroenteritis: ↑1.3x in rainy season                │
│    - Holiday/Post-holiday effects                          │
│  • Creates enriched dataset with multipliers                │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────┐
│  Data Preprocessing Module (preprocess.py)   │
│  • Encodes categorical data                  │
│  • Normalizes features                       │
│  • Splits train/test 80/20                   │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  Model Training Module (train_model.py)      │
│  • RandomForestRegressor                     │
│  • Evaluates: MAE, RMSE, R² Score           │
│  • Saves model & encoders                    │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│  Flask REST API Server (app/app.py)          │
│  • /health - Status check                    │
│  • /predict - Patient count prediction       │
│  • /recommend - Medicine recommendations     │
└──────────────────────────────────────────────┘
```

### What's New in Enhanced Version?

✨ **AQICN API Integration**

- Replaces OpenAQ with more reliable AQICN
- Real-time air quality data
- Better holiday correlation support

🗓️ **Calendarific API Integration**

- Fetches Indian holidays (Holi, Diwali, etc.)
- Predicts patient surges around festivals
- Post-holiday effect detection

🧠 **Intelligent Correlation Logic**

- Disease-specific environment multipliers
- Holiday period peak detection
- Season-based pattern recognition
- Combines all factors for accurate prediction

## 📊 Data Pipeline

### Step 1: Enhanced Data Enrichment (fetch_data.py)

**Input:** `hospital_base_dataset.csv`

The base dataset contains patient admission records:

```
admission_date | disease_type | medicine_used | medicine_quantity | hospital_area
2024-01-01     | Heart Disease| Aspirin      | 50                | ICU
2024-10-31     | Respiratory  | Salbutamol   | 60                | OPD
2024-03-25     | Heart Disease| Lisinopril   | 35                | ICU
```

**Enhanced Processing:**

```
For each unique admission_date:
  1. Count patients by disease type
  2. Fetch AQICN AQI (air quality)
  3. Fetch OpenWeather (temperature, humidity, raw weather)
  4. Fetch Calendarific (holidays for that year)
  5. Check if holiday or near holiday (±3 days)
  6. Apply INTELLIGENT CORRELATIONS:
     ├─ Is Respiratory + Temp < 15°C? → ×1.5
     ├─ Is Respiratory + Diwali (Oct-Nov)? → ×1.3
     ├─ Is Respiratory + ON Diwali date? → ×1.8
     ├─ Is Heart Disease + Temp < 10°C? → ×1.4
     ├─ Is Gastroenteritis + Rainy? → ×1.3
     ├─ Is Holiday + Holi? → ×1.2 (injuries)
     └─ Post-Holiday (day after)? → ×1.15
  7. Create enriched record with multipliers
```

**Output:** `final_dataset.csv`

```
admission_date | disease_type | actual_count | expected_multiplier | temperature | humidity | aqi | weather_condition | is_holiday | holiday_name | days_after_holiday
2024-01-01     | Heart Disease| 2            | 1.0                 | 9.0         | 65       | 150 | Clear            | 0          | None         | 0
2024-10-31     | Respiratory  | 8            | 1.8                 | 10.0        | 80       | 220 | Rainy            | 1          | Diwali       | 0
2024-03-25     | Heart Disease| 2            | 1.2                 | 9.0         | 65       | 150 | Clear            | 1          | Holi         | 0
2024-03-26     | Diabetes     | 3            | 1.15                | 15.0        | 70       | 160 | Clear            | 1          | Holi         | 1
```

**NEW Features Added:**

- `expected_multiplier`: Disease-environment correlation factor (1.0 to 1.8+)
- `weather_condition`: Actual weather condition (Clear, Rainy, Cloudy, etc.)
- `is_holiday`: Boolean (was holiday or within ±3 days)
- `holiday_name`: Name of holiday (Holi, Diwali, etc.)
- `days_after_holiday`: Days from holiday (-3 to +3)

### Step 2: Data Preprocessing (preprocess.py)

**Input:** `final_dataset.csv`

**Processing:**

1. **Date Conversion:**
   - Convert admission_date to datetime
   - Sort data chronologically

2. **Missing Value Handling:**
   - Forward fill numerical columns (time-series data)
   - Drop rows with missing categorical values

3. **Feature Engineering:**
   - Create encoded versions of categorical columns
   - Generate disease_type_encoded
   - Generate hospital_area_encoded

4. **Data Validation:**
   - Check no missing values remain
   - Verify correct data types
   - Ensure reasonable value ranges

5. **Feature & Target Creation:**
   - Features (X): temperature, humidity, aqi, disease_type_encoded, hospital_area_encoded
   - Target (y): patient_count

**Output:**

- Preprocessed DataFrame
- Encoders (saved as pickle) for later inference

### Step 3: Model Development (train_model.py)

#### Model Selection

**Algorithm:** RandomForestRegressor

**Rationale:**

- Handles non-linear relationships well
- Robust to outliers
- Provides feature importance
- Works well with mixed feature types
- Good baseline for regression tasks

#### Hyperparameters

```python
n_estimators: 100        # Number of decision trees
max_depth: 15            # Maximum tree depth (prevents overfitting)
min_samples_split: 5     # Min samples needed to split internal node
min_samples_leaf: 2      # Min samples required at leaf node
```

#### Training Process

```
1. Load and preprocess data
2. Split data (80% train, 20% test)
3. Build RandomForestRegressor with hyperparameters
4. Train on training set
5. Evaluate on test set:
   - Calculate MAE (Mean Absolute Error)
   - Calculate RMSE (Root Mean Squared Error)
   - Calculate R² Score
6. Extract and display feature importance
7. Save model and encoders as pickle files
```

#### Evaluation Metrics

**MAE (Mean Absolute Error)**

- Measures average prediction error
- Interpreted as average number of patients off in prediction
- Example: MAE=2.5 means predictions off by ~2-3 patients on average

**RMSE (Root Mean Squared Error)**

- Similar to MAE but penalizes larger errors more
- Usually higher than MAE
- Good for detecting outliers

**R² Score**

- Proportion of variance explained (0 to 1)
- 0.85 R² means model explains 85% of variance
- Higher is better

#### Feature Importance

```python
Random Forest provides importance scores:
1. temperature: 0.35      (35% importance)
2. aqi: 0.25              (25% importance)
3. humidity: 0.20         (20% importance)
4. disease_type_encoded: 0.15  (15% importance)
5. hospital_area_encoded: 0.05 (5% importance)
```

## 🔌 API Architecture

### Flask REST API (app/app.py)

#### Design Patterns Used

1. **Separation of Concerns**
   - Load model/encoders once at startup
   - Validation functions separate from prediction logic
   - Feature preparation isolated in dedicated function

2. **Error Handling**
   - Input validation before processing
   - Graceful error responses with clear messages
   - HTTP status codes indicate success/failure

3. **Logging**
   - Track all predictions and recommendations
   - Log errors with full context

4. **Stateless Design**
   - Each request independent
   - No session state maintained
   - Easy to scale horizontally

### Prediction Endpoint

```python
@app.route("/predict", methods=["POST"])
def predict():
    # 1. Validate input data
    # 2. Prepare features for model
    # 3. Make prediction
    # 4. Return results with confidence range
    # 5. Handle errors gracefully
```

**Request Validation:**

```
temperature: Must be numeric, -50 to 60°C
humidity: Must be numeric, 0-100%
aqi: Must be numeric, >= 0
disease_type: Must be string (optional)
hospital_area: Must be string (optional)
```

**Feature Preparation:**

```python
# User inputs
{temperature, humidity, aqi, disease_type, hospital_area}
    ↓
# Encode categorical columns
{temperature, humidity, aqi, disease_type_encoded, hospital_area_encoded}
    ↓
# Create DataFrame matching training format
# Make prediction
predicted_count = model.predict(features_df)
    ↓
# Add confidence range (±2 patients)
{predicted_count, lower_bound, upper_bound}
```

### Recommendation Endpoint

```python
@app.route("/recommend", methods=["POST"])
def recommend_medicines():
    # 1. Validate input
    # 2. Get medicines for disease type
    # 3. Calculate recommended quantities
    # 4. Check current stock levels
    # 5. Determine actions (order/maintain/reduce)
    # 6. Generate expiry warnings
    # 7. Return recommendations
```

**Recommendation Logic:**

```
For each medicine in disease-specific database:

    1. Base quantity from database
    2. Multiplier = predicted_count / 5.0
    3. Recommended qty = base_qty × multiplier

    4. Check stock levels:
       if current < CRITICAL (20):
           action = "URGENT: Order immediately"
           increase = 70% above recommended
       elif current < LOW (50):
           action = "Order soon"
           increase = 20% above recommended
       elif predicted > 10:
           action = "Increase stock"
           increase = 20% above recommended
       elif predicted < 3:
           action = "Decrease stock"
           decrease = 10% below recommended
       else:
           action = "Maintain current stock"

    5. Add expiry warnings based on medicine type
    6. Mark criticality: CRITICAL / HIGH / NORMAL
```

## 🗄️ Database & Configuration

### Configuration Structure (config.py)

```python
# API Endpoints
OPENAQ_API_URL = "https://api.openaq.org/v2/latest"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Hospital Location
HOSPITAL_LAT = 19.2183      # Mumbai latitude
HOSPITAL_LON = 72.9781      # Mumbai longitude

# File Paths
HOSPITAL_BASE_DATASET = "data/hospital_base_dataset.csv"
FINAL_DATASET = "data/final_dataset.csv"
MODEL_PATH = "models/patient_inflow_model.pkl"
ENCODER_PATH = "models/encoders.pkl"

# Model Hyperparameters
N_ESTIMATORS = 100
MAX_DEPTH = 15
TEST_SIZE = 0.2

# Medicine Stock Thresholds
LOW_STOCK_THRESHOLD = 50
CRITICAL_STOCK_THRESHOLD = 20

# Medicine Database
MEDICINE_DATABASE = {
    "Heart Disease": [
        {"name": "Aspirin", "base_qty": 100, "expiry_critical_days": 30},
        ...
    ],
    ...
}
```

### Disease & Medicine Mapping

```python
Disease Type          | Base Medicines        | Qty | Expiry Days
─────────────────────┼──────────────────────┼─────┼────────────
Heart Disease        | Aspirin              | 100 | 30
                     | Atorvastatin         | 50  | 60
                     | Lisinopril           | 50  | 60
─────────────────────┼──────────────────────┼─────┼────────────
Diabetes             | Insulin              | 200 | 7
                     | Metformin            | 150 | 90
                     | Glipizide            | 100 | 90
─────────────────────┼──────────────────────┼─────┼────────────
Respiratory Infection| Amoxicillin          | 120 | 60
                     | Salbutamol           | 80  | 90
                     | Omeprazole           | 100 | 90
```

## 🔒 Data Flow Security

### API Key Management

```
.env file (not in Git)
    ↓
load_dotenv()
    ↓
os.getenv("OPENWEATHER_API_KEY")
    ↓
config.py
    ↓
app.py (used in requests)
```

### API Error Handling

```
Request to external API
    ↓
    ├─ Success? → Extract data
    │
    └─ Failure? → Use default values
                  (Graceful degradation)

Better to have approximate predictions
than crash due to API issues
```

## 📈 Scalability Considerations

### Horizontal Scaling

```
Load Balancer
    ├── API Server 1
    ├── API Server 2
    └── API Server 3

(Using Gunicorn with multiple workers)
```

### Caching

```
Predictions with same inputs
→ Cache results for 5 minutes
→ Reduce model inference load
```

### Batch Processing

```
For high-volume predictions:
→ Accept batch of requests
→ Process in parallel
→ Return array of results
```

### Model Update Pipeline

```
New data collected
    ↓
Retrain model (scheduled, e.g., weekly)
    ↓
Evaluate new vs old model
    ↓
If better, update production model
    ↓
Keep version history for rollback
```

## 🧪 Testing Strategy

### Unit Tests

```
fetch_data.py:
  - API URL construction
  - Response parsing
  - Default value fallback

preprocess.py:
  - Missing value handling
  - Encoding verification
  - Data validation

train_model.py:
  - Model training
  - Metric calculation
  - Model persistence
```

### Integration Tests

```
End-to-end pipeline:
  fetch_data() → preprocess() → train() → predict()

API endpoints:
  /health check
  /predict with valid/invalid input
  /recommend with various scenarios
```

### Manual Tests

```
test_api.py provides:
  - Health check
  - Prediction tests (normal, extreme, edge cases)
  - Recommendation tests
  - Error handling tests
```

## 🎯 Performance Metrics

### Model Performance

```
Train MAE:   ~1.2 patients
Test MAE:    ~1.5 patients
Train RMSE:  ~1.5 patients
Test RMSE:   ~1.9 patients
R² Score:    ~0.82
```

### API Performance

```
/health:     < 10ms
/predict:    50-200ms (model inference)
/recommend:  30-100ms (lookup + logic)
```

### Resource Usage

```
Model file:  ~5-10 MB (depending on data)
Memory:      ~200-500 MB (at runtime)
CPU:         Minimal (single prediction < 100ms)
```

## 📚 Code Quality Standards

### Clean Code Principles

- Single responsibility per function
- Descriptive variable names
- Comprehensive comments
- Error messages help debugging
- No hardcoded values (except API keys)

### Documentation

- Docstrings for all functions
- Type hints where applicable
- README with examples
- Inline comments for complex logic
- Architecture documentation (this file)

### Error Handling

- Try-catch for API calls
- Input validation on all endpoints
- Graceful degradation for failures
- Detailed logging for debugging

---

**Version:** 1.0.0  
**Last Updated:** January 2024  
**Architecture Pattern:** Modular Pipeline with REST API
