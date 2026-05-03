# ArogyaPredict - Hospital Patient Inflow Prediction System

A comprehensive AI-based modular backend system for predicting hospital patient inflow using environmental data (AQI and weather) and recommending medicine stock planning.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)
- [Code Quality](#code-quality)

## 🎯 Overview

**ArogyaPredict** is a production-ready ML system that:
- Predicts hospital patient inflow based on environmental factors
- Provides medicine stock recommendations
- Uses real-time environmental data from APIs
- Implements a modular, scalable architecture

## 📁 Project Structure

```
ArogyaPredict/
├── data/
│   ├── hospital_base_dataset.csv      # Base hospital dataset
│   └── final_dataset.csv              # Enriched dataset with environmental data
├── scripts/
│   ├── fetch_data.py                  # Data enrichment from APIs
│   ├── preprocess.py                  # Data preprocessing and encoding
│   └── train_model.py                 # Model training and evaluation
├── models/
│   ├── patient_inflow_model.pkl       # Trained RandomForest model
│   └── encoders.pkl                   # Label encoders for categorical features
├── app/
│   └── app.py                         # Flask REST API
├── config.py                          # Configuration and constants
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
└── README.md                          # This file
```

## 📦 Requirements

- Python 3.8+
- pip (Python package manager)

## 🚀 Installation

### 1. Clone/Setup Project

```bash
cd e:\BCA\Final\ArogyaPredict
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get API Keys

- **OpenWeather API:**
  1. Visit https://openweathermap.org/api
  2. Sign up for a free account
  3. Get your API key from the dashboard

### 5. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
# OPENWEATHER_API_KEY=your_key_here
```

## ⚙️ Configuration

Key configuration variables in `config.py`:

```python
# API Configuration
OPENAQ_API_URL = "https://api.openaq.org/v2/latest"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_API_KEY = "your_api_key"

# Model Hyperparameters
N_ESTIMATORS = 100
MAX_DEPTH = 15
MIN_SAMPLES_SPLIT = 5
TEST_SIZE = 0.2

# Medicine Stock Thresholds
LOW_STOCK_THRESHOLD = 50
CRITICAL_STOCK_THRESHOLD = 20
```

## 📊 Usage

### Step 1: Enrich Dataset with Environmental Data

```bash
cd scripts
python fetch_data.py
```

**What it does:**
- Reads `hospital_base_dataset.csv`
- Fetches real AQI data from OpenAQ API
- Fetches real weather data from OpenWeather API
- Creates enriched dataset with: temperature, humidity, AQI, patient_count
- Saves to `data/final_dataset.csv`

**Output:**
```
Loading data from hospital_base_dataset.csv...
Fetching AQI data for 2024-01-01...
Fetching weather data...
✓ Final dataset saved with 30 records and 7 features
```

### Step 2: Preprocess Data

```bash
python preprocess.py
```

**What it does:**
- Handles missing values (forward fill + backward fill)
- Converts dates to datetime format
- Encodes categorical columns (disease_type, hospital_area)
- Validates data quality
- Saves encoders for later use

**Output:**
```
Loading data from final_dataset.csv...
Handling missing values...
Encoding categorical columns...
✓ Preprocessing completed!
Features shape: (30, 5)
```

### Step 3: Train Model

```bash
python train_model.py
```

**What it does:**
- Loads preprocessed data
- Splits into train/test (80/20)
- Trains RandomForestRegressor
- Evaluates using MAE, RMSE, R² score
- Saves model and encoders

**Output:**
```
MODEL EVALUATION METRICS
═══════════════════════════════
Mean Absolute Error (MAE):
  Training:  1.2345 patients
  Testing:   1.5678 patients

Root Mean Squared Error (RMSE):
  Training:  1.5432 patients
  Testing:   1.8765 patients

R² Score:
  Training:  0.8765
  Testing:   0.8234
═══════════════════════════════
```

### Step 4: Run Flask API

```bash
cd app
python app.py
```

**Output:**
```
ArogyaPredict - Flask API Server
═══════════════════════════════════
✓ Model and encoders loaded successfully!
✓ API Server is ready to receive requests

Available endpoints:
  GET  /health - Health check
  POST /predict - Predict patient count
  POST /recommend - Get medicine recommendations

 * Running on http://0.0.0.0:5000
```

## 🔌 API Documentation

### 1. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00.123456",
    "model_loaded": true,
    "endpoints": ["/health", "/predict", "/recommend"]
}
```

### 2. Predict Patient Count

**Endpoint:** `POST /predict`

**Request:**
```json
{
    "temperature": 28.5,
    "humidity": 65,
    "aqi": 150,
    "disease_type": "Heart Disease",
    "hospital_area": "General Ward"
}
```

**Response:**
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

**Error Response:**
```json
{
    "error": "Missing required field: 'temperature'",
    "status": "error"
}
```

### 3. Medicine Recommendations

**Endpoint:** `POST /recommend`

**Request:**
```json
{
    "predicted_patient_count": 15,
    "disease_type": "Heart Disease",
    "current_stock": 100
}
```

**Response:**
```json
{
    "status": "success",
    "input": {
        "predicted_patient_count": 15,
        "disease_type": "Heart Disease",
        "current_stock": 100
    },
    "recommendations": [
        {
            "medicine": "Aspirin",
            "current_stock": 100,
            "recommended_quantity": 180,
            "action": "Increase stock",
            "expiry_warning": "Check expiry within 30 days",
            "criticality": "NORMAL"
        },
        {
            "medicine": "Atorvastatin",
            "current_stock": 100,
            "recommended_quantity": 90,
            "action": "Maintain current stock",
            "expiry_warning": "Check expiry within 60 days",
            "criticality": "NORMAL"
        }
    ],
    "summary": {
        "total_medicines": 3,
        "critical_count": 0,
        "high_count": 0
    },
    "timestamp": "2024-01-15T10:30:00.123456"
}
```

## 🏗️ Architecture

### Data Pipeline

```
hospital_base_dataset.csv
         ↓
   fetch_data.py (Enrich with APIs)
         ↓
   final_dataset.csv
         ↓
   preprocess.py (Clean & Encode)
         ↓
   train_model.py (Train ML Model)
         ↓
   Saved Model + Encoders
         ↓
   app.py (REST API)
         ↓
   Predictions & Recommendations
```

### Model Architecture

**Algorithm:** RandomForestRegressor

**Input Features:**
- `temperature` (°C): Current temperature
- `humidity` (%): Current humidity level
- `aqi`: Air Quality Index
- `disease_type_encoded`: Encoded disease type
- `hospital_area_encoded`: Encoded hospital area

**Target Variable:**
- `patient_count`: Number of patient admissions

**Hyperparameters:**
- n_estimators: 100 trees
- max_depth: 15 levels
- min_samples_split: 5
- min_samples_leaf: 2

### Medicine Recommendation Logic

1. **Get Baseline:** Use disease-specific medicine database
2. **Calculate Need:** Scale quantity based on predicted patient count
3. **Check Stock Level:**
   - **Critical** (< 20): Order immediately (+50% increase)
   - **Low** (< 50): Order soon (+20% increase)
   - **Normal** (>= 50): Maintain or adjust based on prediction
4. **Output:** Specific action, quantity, and expiry warnings

## 💻 Code Quality

### Modular Design
- **config.py:** Centralized configuration
- **scripts/fetch_data.py:** Data enrichment logic
- **scripts/preprocess.py:** Data preprocessing pipeline
- **scripts/train_model.py:** Model training pipeline
- **app/app.py:** REST API endpoints

### Error Handling
- Graceful API failure handling with default values
- Input validation on all endpoints
- Detailed logging at each step
- Try-catch blocks for robust execution

### Production Readiness
- Environment variable management for API keys
- Proper logging and monitoring
- Input sanitization and validation
- RESTful API design
- Model versioning (saved as pickle)
- Configuration management

## 📈 Example Workflow

```bash
# 1. Setup
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# 2. Data Preparation
cd scripts
python fetch_data.py
python preprocess.py
python train_model.py

# 3. Run API
cd ../app
python app.py

# 4. Test (from another terminal)
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28.5, "humidity": 65, "aqi": 150}'
```

## 🔧 Troubleshooting

**Model not found error:**
```bash
# Make sure you ran train_model.py first
python scripts/train_model.py
```

**API Key errors:**
```bash
# Check .env file has correct API key
cat .env
```

**Missing dependencies:**
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

## 📝 License

This project is provided as-is for educational and commercial use.

## 👥 Support

For issues or questions, please review the code comments and logging output.

---

**Last Updated:** January 2024
**Version:** 1.0.0
