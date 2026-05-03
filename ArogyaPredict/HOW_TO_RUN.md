# ArogyaPredict - HOW TO RUN (Complete Guide)

## 📋 Overview

**ArogyaPredict** predicts hospital patient inflow based on:

- **Weather data** (temperature, humidity)
- **Air Quality Index (AQI)** from pollution
- **Holidays & Events** (Holi, Diwali, etc.)
- **Historical patient data**

Then it **recommends medicine restocking** based on predicted patient surge.

---

## 🚀 QUICK START (5 Minutes)

### 1. Open Terminal

```bash
# Navigate to project
cd e:\BCA\Final\ArogyaPredict
```

### 2. Create Virtual Environment (First time only)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install All Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Environment Setup

```bash
# Check if .env file exists
dir .env

# If not found, it was already created
```

### 5. Run Data Processing Pipeline

```bash
# Step 1: Enrich dataset with holiday/weather/AQI data
python scripts/fetch_data.py

# Step 2: Preprocess data for model training
python scripts/preprocess.py

# Step 3: Train machine learning model
python scripts/train_model.py

# Step 4: Start Flask API server
python app/app.py
```

**You will see:**

```
✓ Data enrichment completed successfully!
✓ Data preprocessing completed successfully!
✓ Model training completed successfully!
✓ Flask API running on http://127.0.0.1:5000
```

---

## 📝 Detailed Execution Steps

### **STEP 1: Data Enrichment (Fetch API Data)**

```bash
python scripts/fetch_data.py
```

**What it does:**

1. ✓ Reads `hospital_base_dataset.csv`
2. ✓ Fetches AQICN AQI (Air Quality)
3. ✓ Fetches OpenWeather data (temperature, humidity)
4. ✓ Fetches Calendarific holidays (Holi, Diwali, etc.)
5. ✓ Calculates disease-weather correlations:
   - **Respiratory Infection**: ↑ 1.5x in cold weather, 1.8x during Diwali
   - **Heart Disease**: ↑ 1.4x in extreme cold
   - **Gastroenteritis**: ↑ 1.3x during rainy season
6. ✓ Saves enriched dataset to `data/final_dataset.csv`

**Output example:**

```
admission_date,disease_type,actual_patient_count,expected_multiplier,temperature,humidity,aqi,is_holiday,holiday_name
2024-10-01,Respiratory Infection,3,1.5,12.5,75,180,False,None
2024-10-31,Respiratory Infection,8,1.8,10.0,80,220,True,Diwali
2024-03-25,Heart Disease,2,1.2,9.0,65,150,True,Holi
```

---

### **STEP 2: Data Preprocessing**

```bash
python scripts/preprocess.py
```

**What it does:**

1. ✓ Loads enriched dataset
2. ✓ Encodes categorical variables (disease types, weather)
3. ✓ Normalizes numerical features (temperature, AQI)
4. ✓ Splits data: 80% training, 20% testing
5. ✓ Saves preprocessed data to `data/final_dataset.csv` (overwritten, with encoded columns)

**How to interpret the data:**

- `disease_type_encoded`: 0-9 for different diseases
- `is_holiday_encoded`: 0 or 1
- `weather_condition_encoded`: 0-4 for different conditions

---

### **STEP 3: Train ML Model**

```bash
python scripts/train_model.py
```

**What it does:**

1. ✓ Loads preprocessed data
2. ✓ Trains **RandomForestRegressor** model
3. ✓ Evaluates with metrics:
   - **MAE** (Mean Absolute Error) - average error in patient count
   - **RMSE** (Root Mean Squared Error) - how far off predictions are
   - **R² Score** - model accuracy (0-1, higher is better)
4. ✓ Saves model to `models/patient_inflow_model.pkl`
5. ✓ Saves encoders to `models/encoders.pkl`

**Example output:**

```
Model Performance:
  MAE: 1.23 patients
  RMSE: 1.87 patients
  R² Score: 0.92 (92% accurate)
```

---

### **STEP 4: Run Prediction API**

```bash
python app/app.py
```

**API starts on:** `http://127.0.0.1:5000`

---

## 🔌 Using the API

### **Test 1: Predict Patient Count**

```bash
# In another terminal, run:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "disease_type": "Respiratory Infection",
    "temperature": 12.5,
    "humidity": 75,
    "aqi": 180,
    "weather_condition": "Rainy",
    "is_holiday": 1
  }'
```

**Response:**

```json
{
  "disease_type": "Respiratory Infection",
  "predicted_patient_count": 6,
  "confidence": 0.92,
  "message": "High patient surge expected during Diwali season"
}
```

### **Test 2: Get Medicine Recommendations**

```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "disease_type": "Respiratory Infection",
    "predicted_patient_count": 6
  }'
```

**Response:**

```json
{
  "disease_type": "Respiratory Infection",
  "medicines": [
    {
      "name": "Amoxicillin",
      "required_quantity": 420,
      "status": "RESTOCK_URGENT"
    },
    {
      "name": "Salbutamol",
      "required_quantity": 280,
      "status": "RESTOCK_URGENT"
    }
  ]
}
```

---

## 📊 Understanding .md Files

### **What are .md files?**

- **`.md` = Markdown files** - They're documentation files that GitHub/VS Code display beautifully
- They use simple formatting: `#` for headers, `**bold**`, `- bullets`, etc.

### **Key .md Files in Your Project:**

| File                      | Purpose                                  |
| ------------------------- | ---------------------------------------- |
| `README.md`               | Project overview & setup instructions    |
| `QUICK_START.md`          | Fast 5-minute start guide                |
| `ARCHITECTURE.md`         | How the system works (data flow)         |
| `API_TESTING_EXAMPLES.md` | Sample API requests & responses          |
| `HOW_TO_RUN.md`           | **This file** - Detailed execution steps |
| `.env.example`            | Environment variable template            |

---

## 🔧 Configuration Files

### **`.env` File**

Controls API keys and settings:

```
OPENWEATHER_API_KEY=413fb69e2131d708599a7ce339e630e7
AQICN_API_KEY=7e966d5083c3e1aa50aa28e4b369c2234c883b3b
CALENDARIFIC_API_KEY=Sa1OPrP0KN3x4G0BETGRp2muiCDaPWyl
HOSPITAL_LAT=19.2183
HOSPITAL_LON=72.9781
HOSPITAL_COUNTRY=IN
```

### **`config.py` File**

Python configuration (medicine database, thresholds, etc.)

---

## 📂 Project Directory Structure

```
ArogyaPredict/
├── data/
│   ├── hospital_base_dataset.csv          # Original patient data
│   └── final_dataset.csv                  # Enriched with weather/holidays/AQI
├── scripts/
│   ├── fetch_data.py                      # Fetch API data (Step 1)
│   ├── preprocess.py                      # Prepare data (Step 2)
│   ├── train_model.py                     # Train model (Step 3)
│   └── analyze_data.py                    # (Optional) Data analysis
├── models/
│   ├── patient_inflow_model.pkl           # Trained model
│   └── encoders.pkl                       # Data encoders
├── app/
│   └── app.py                             # Flask API (Step 4)
├── config.py                              # Configuration
├── requirements.txt                       # Dependencies
├── .env                                   # API keys (SECRET!)
├── .env.example                           # Template (share this, not .env)
└── README.md                              # Main documentation
```

---

## 🛠️ Troubleshooting

### **Error: "Could not find hospital_base_dataset.csv"**

```bash
# Solution: Make sure you're in the right directory
cd e:\BCA\Final\ArogyaPredict
python scripts/fetch_data.py
```

### **Error: "API Key Invalid"**

```bash
# Solution: Check your .env file
cat .env

# If API key is wrong, update it:
# 1. Open .env file
# 2. Fix the key
# 3. Save
# 4. Run script again
```

### **Error: "ModuleNotFoundError: No module named 'pandas'"**

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### **Error: "Port 5000 already in use"**

```bash
# Solution: Use different port or kill the process
# Windows:
netstat -ano | findstr :5000

# Then: taskkill /PID <PID> /F
```

---

## 📈 Example Workflow

```bash
# 1. Start terminal
cd e:\BCA\Final\ArogyaPredict

# 2. Activate environment
venv\Scripts\activate

# 3. Run pipeline
python scripts/fetch_data.py    # Takes 1-2 min (fetches APIs)
python scripts/preprocess.py    # Takes 10 seconds
python scripts/train_model.py   # Takes 30 seconds

# 4. Start API
python app/app.py               # Runs on http://127.0.0.1:5000

# 5. In another terminal, test:
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"disease_type": "Respiratory Infection", "temperature": 12, "humidity": 75, "aqi": 180, "weather_condition": "Rainy", "is_holiday": 1}'
```

---

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] `pip install -r requirements.txt` completed
- [ ] `.env` file has your API keys
- [ ] `python scripts/fetch_data.py` → SUCCESS
- [ ] `python scripts/preprocess.py` → SUCCESS
- [ ] `python scripts/train_model.py` → SUCCESS (shows R² score)
- [ ] `python app/app.py` → SUCCESS (API running)
- [ ] API endpoint responds with predictions

---

## 💡 Your Project's Intelligence

This system **intelligently predicts** patient surges by correlating:

1. **Weather patterns** → respiratory increases in cold
2. **Air pollution (AQI)** → respiratory infections spike when AQI > 200
3. **Festival seasons**:
   - **Holi** (March) → injuries from celebrations (+20%)
   - **Diwali** (Oct-Nov) → severe respiratory issues (+80%, pollution spike)
   - **Post-holiday** → delayed hospital visits (+15%)

4. **Season-specific diseases**:
   - Cold months → heart disease (+40%)
   - Rainy season → waterborne diseases (+30%)
   - Summer → heat-related issues (+25%)

Then it **automatically restocks medicines** based on these predictions!

---

**Need help? Check:**

- [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
- [API_TESTING_EXAMPLES.md](API_TESTING_EXAMPLES.md) - More API examples
- [config.py](config.py) - All configuration options
