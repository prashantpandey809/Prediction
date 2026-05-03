# SETUP.md - Complete Project Setup Guide

## 🎯 What is ArogyaPredict?

**ArogyaPredict** is an AI-powered hospital management system that:

1. **Predicts** patient inflow based on:
   - Weather conditions
   - Air quality (AQI)
   - Holidays & events
   - Historical data

2. **Recommends** medicine restocking based on predicted patient surge

3. **Analyzes** correlations between environmental factors and disease patterns

---

## 📚 Understanding .md Files

### What are .md files?

`.md` = **Markdown** files - they're documentation files for humans to read.

**Why use .md?**

- GitHub displays them beautifully with formatting
- VS Code shows them with proper highlighting
- They're plain text, so any editor works
- Use simple syntax: `#` headers, `**bold**`, `- bullets`

### .md Files in This Project

| File                      | Purpose                            | When to Read               |
| ------------------------- | ---------------------------------- | -------------------------- |
| `README.md`               | Project intro & features           | First time setup           |
| `HOW_TO_RUN.md`           | **Step-by-step execution**         | **Before running code**    |
| `QUICK_START.md`          | 5-minute fast start                | If in hurry                |
| `ARCHITECTURE.md`         | How data flows through system      | Understanding design       |
| `API_TESTING_EXAMPLES.md` | Sample API requests/responses      | Testing the API            |
| `setup.py`                | Python package setup file          | Python distribution (skip) |
| `.env.example`            | Template for environment variables | Configuration              |
| `index.md`                | Project index/navigation           | Finding files              |

---

## 🛠️ Prerequisites

Before you start, make sure you have:

- **Python 3.8+** installed

  ```bash
  python --version  # Should show 3.8 or higher
  ```

- **pip** (Python package manager)

  ```bash
  pip --version
  ```

- **Git** (optional, for version control)
  ```bash
  git --version
  ```

### Installation Check:

```bash
# Windows - Test all tools
python --version
pip --version
node --version    # Optional

# If any show "not found", install that tool first
```

---

## 📋 Your API Keys (Already Added)

The following keys are configured in `.env`:

| API              | Key                                        | Purpose                       |
| ---------------- | ------------------------------------------ | ----------------------------- |
| **OpenWeather**  | `413fb69e2131d708599a7ce339e630e7`         | Weather data (temp, humidity) |
| **AQICN**        | `7e966d5083c3e1aa50aa28e4b369c2234c883b3b` | Air Quality Index             |
| **Calendarific** | `Sa1OPrP0KN3x4G0BETGRp2muiCDaPWyl`         | Holidays & events             |

---

## 🚀 Complete Setup Steps

### **Step 1: Navigate to Project (2 seconds)**

```bash
cd e:\BCA\Final\ArogyaPredict

# Verify by checking these files exist:
dir data/hospital_base_dataset.csv
dir requirements.txt
dir .env
```

### **Step 2: Create Virtual Environment (30 seconds)** ⭐ IMPORTANT

**Why?** Virtual environments isolate Python packages so they don't conflict.

```bash
# Windows
python -m venv venv

# Check it was created
dir venv   # Should show Scripts, Lib, etc.
```

### **Step 3: Activate Virtual Environment**

**Every time you work on this project, activate first!**

```bash
# Windows
venv\Scripts\activate

# You should see (venv) in your terminal now
# (venv) PS C:\...>

# Linux/Mac
source venv/bin/activate
```

### **Step 4: Install All Dependencies (1-2 minutes)**

```bash
pip install -r requirements.txt

# This installs:
# - pandas (data handling)
# - numpy (math)
# - scikit-learn (machine learning)
# - flask (web API)
# - requests (fetch APIs)
# - python-dotenv (environment variables)
# - joblib (save/load models)
# - pytz (timezone handling)
# - gunicorn (production server)
```

### **Step 5: Verify Installation**

```bash
# Test that all packages installed correctly
python -c "import pandas, numpy, sklearn, flask, requests; print('✓ All packages installed!')"
```

### **Step 6: Run the Full Pipeline**

```bash
# Run in this order:

# 1. Fetch data from APIs (1-2 minutes)
python scripts/fetch_data.py

# Expected output:
# ✓ Enriched dataset saved: data/final_dataset.csv
# ✓ Total enriched records: 150+

# 2. Preprocess data (10 seconds)
python scripts/preprocess.py

# Expected output:
# ✓ Data preprocessing completed successfully!

# 3. Train ML model (30 seconds)
python scripts/train_model.py

# Expected output:
# Model Performance:
#   MAE: 1.23 patients
#   RMSE: 1.87 patients
#   R² Score: 0.92

# 4. Start API server (runs forever)
python app/app.py

# Expected output:
# Running on http://127.0.0.1:5000
# Press CTRL+C to stop
```

---

## 🔍 Understanding the Execution Order

### Why does the order matter?

```
Step 1: fetch_data.py
   ↓
   Creates: data/final_dataset.csv (enriched with weather/AQI/holidays)
   ↓
Step 2: preprocess.py
   ↓
   Uses: data/final_dataset.csv
   Creates: Encoded features for ML
   ↓
Step 3: train_model.py
   ↓
   Uses: Preprocessed data
   Creates: models/patient_inflow_model.pkl (trained model)
   ↓
Step 4: app.py (Flask API)
   ↓
   Uses: models/patient_inflow_model.pkl
   Provides: HTTP endpoints for predictions
```

If you skip a step:

- ❌ You'll get "FileNotFoundError" or "Model not found"
- ✅ Do each step in order

---

## 📝 What Each Script Does

### **1️⃣ `scripts/fetch_data.py` - API Data Collection**

**Input:** `data/hospital_base_dataset.csv` (patient admissions)

**Process:**

- Fetches AQICN AQI (air quality) for each date
- Fetches OpenWeather data (temperature, humidity)
- Fetches Calendarific holidays (Holi, Diwali, etc.)
- Calculates disease-environment correlations
- Applies intelligent multipliers:
  - Respiratory: 1.5x-1.8x in cold/Diwali
  - Heart Disease: 1.4x in extreme cold
  - Gastroenteritis: 1.3x in rainy season

**Output:** `data/final_dataset.csv`

**Sample data:**

```
admission_date,disease_type,actual_patient_count,expected_multiplier,temperature,aqi,is_holiday,holiday_name
2024-10-31,Respiratory Infection,8,1.8,10.0,220,1,Diwali
2024-03-25,Heart Disease,2,1.2,9.0,150,1,Holi
```

---

### **2️⃣ `scripts/preprocess.py` - Data Preparation**

**Input:** `data/final_dataset.csv`

**Process:**

- Encodes categorical variables (disease types, weather conditions)
- Normalizes numerical features (0-1 scale)
- Splits into 80% training, 20% testing
- Removes missing values

**Output:** Preprocessed data ready for machine learning

**Example transformations:**

```
disease_type: "Respiratory Infection" → 2
weather_condition: "Rainy" → 3
is_holiday: True → 1
```

---

### **3️⃣ `scripts/train_model.py` - Model Training**

**Input:** Preprocessed data

**Process:**

- Train RandomForestRegressor (ML model)
- Evaluate with metrics:
  - **MAE**: Average prediction error
  - **RMSE**: Error spread
  - **R²**: Accuracy (0-1, higher better)
- Save model to disk

**Output:**

- `models/patient_inflow_model.pkl` (trained model)
- `models/encoders.pkl` (data encoders)

**Good R² score:** 0.85-0.95 (85-95% accurate)

---

### **4️⃣ `app/app.py` - Flask REST API**

**Input:** Trained model + user requests

**Process:**

- Loads trained model from disk
- Provides 3 endpoints:
  - `/predict` (POST) → Predict patient count
  - `/recommend` (POST) → Get medicine recommendations
  - `/health` (GET) → Check API status

**Output:** JSON responses with predictions

**Example:**

```
POST /predict
Input: { "disease_type": "Respiratory", "temp": 12, "aqi": 180, ... }
Output: { "predicted_patients": 6, "confidence": 0.92, ... }
```

---

## 📊 Configuration Files

### **`.env` File** (API Keys & Settings)

```
OPENWEATHER_API_KEY=413fb69e2131d708599a7ce339e630e7
AQICN_API_KEY=7e966d5083c3e1aa50aa28e4b369c2234c883b3b
CALENDARIFIC_API_KEY=Sa1OPrP0KN3x4G0BETGRp2muiCDaPWyl
HOSPITAL_LAT=19.2183
HOSPITAL_LON=72.9781
HOSPITAL_COUNTRY=IN
FLASK_ENV=production
FLASK_DEBUG=False
```

**Never commit `.env` to Git!** (Contains secrets)

### **`config.py` File** (Python Configuration)

```python
# API URLs
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
AQICN_API_URL = "https://api.waqi.info/feed/geo"

# Thresholds
LOW_STOCK_THRESHOLD = 50
CRITICAL_STOCK_THRESHOLD = 20

# Medicine database
MEDICINE_DATABASE = {
    "Respiratory Infection": ["Amoxicillin", "Salbutamol", ...],
    "Heart Disease": ["Aspirin", "Atorvastatin", ...],
    ...
}
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# 1. Check Python
python --version                    # Should be 3.8+

# 2. Check virtual environment
venv\Scripts\activate
(venv) echo "✓ Activated"           # Should show (venv) prefix

# 3. Check dependencies
pip list | findstr pandas          # Should include pandas 2.0.3

# 4. Check API keys
cat .env                            # Should show 3 API keys

# 5. Check data files
dir data\hospital_base_dataset.csv  # Should exist

# 6. Run first script
python scripts/fetch_data.py        # Should create final_dataset.csv

# 7. Check model starts
python app/app.py                   # Should start on http://127.0.0.1:5000
```

---

## 🐛 Common Issues & Solutions

### **Issue: "Python not found"**

```bash
# Solution: Install Python from python.org
# Then restart terminal and try again
python --version
```

### **Issue: "No module named 'pandas'"**

```bash
# Solution: Install requirements
pip install -r requirements.txt

# Or reinstall manually
pip install pandas==2.0.3
```

### **Issue: "ModuleNotFoundError in config.py"**

```bash
# Make sure you're using the activated venv:
venv\Scripts\activate
python scripts/fetch_data.py
```

### **Issue: "API Key invalid"**

```bash
# Check your .env file has correct keys:
cat .env

# If wrong, update it and save
# Make sure there are no spaces: `KEY=value` not `KEY = value`
```

### **Issue: "Port 5000 in use"**

```bash
# Windows: Find and kill the process
netstat -ano | findstr :5000
# taskkill /PID <NUMBER> /F

# Linux/Mac:
lsof -i :5000
# kill <PID>

# Or use different port:
python app/app.py --port 8000
```

---

## 💾 Files Generated During Setup

After running all scripts, you'll have:

```
models/
  ├── patient_inflow_model.pkl      # Trained model (~2MB)
  └── encoders.pkl                  # Encoders (~1KB)

data/
  ├── hospital_base_dataset.csv     # Original data (you provide this)
  └── final_dataset.csv             # Enriched data (created by fetch_data.py)
```

**Don't delete these files!** The API needs them.

---

## 🚀 After Setup: What's Next?

1. **Test the API** → See [HOW_TO_RUN.md](HOW_TO_RUN.md)
2. **Make predictions** → See [API_TESTING_EXAMPLES.md](API_TESTING_EXAMPLES.md)
3. **Understand the system** → See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Modify for your hospital:**
   - Change `HOSPITAL_LAT/LON` to your hospital location
   - Update `MEDICINE_DATABASE` with your medicines
   - Add more disease types if needed

---

## 📞 Need Help?

- **Setup issues?** → Re-read this file
- **How to run?** → See [HOW_TO_RUN.md](HOW_TO_RUN.md)
- **API examples?** → See [API_TESTING_EXAMPLES.md](API_TESTING_EXAMPLES.md)
- **Architecture?** → See [ARCHITECTURE.md](ARCHITECTURE.md)

---

**You're all set! Now go to [HOW_TO_RUN.md](HOW_TO_RUN.md) to execute the project.** ✨
