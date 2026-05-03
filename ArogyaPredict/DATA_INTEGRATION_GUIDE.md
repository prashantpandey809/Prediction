# Data Integration Guide - ArogyaPredict

## 📊 Integrated Hospital Datasets

The ArogyaPredict project now includes and integrates two comprehensive hospital datasets:

### 1. **Base Hospital Dataset** (`hospital_base_dataset.csv`)
- **Records:** 30 patient admissions
- **Features:** admission_date, disease_type, medicine_used, medicine_quantity, hospital_area
- **Purpose:** Primary dataset for training patient inflow prediction model
- **Use Case:** Time-series analysis of hospital admissions and medicine usage

### 2. **Hospital Analysis Dataset** (`hospital_analysis_dataset.csv`)
- **Records:** 49 patient cases  
- **Features:** Patient_ID, Age, Gender, Condition, Procedure, Cost, Length_of_Stay, Readmission, Outcome, Satisfaction
- **Purpose:** Rich clinical data for insights and cross-analysis
- **Use Case:** Demographic analysis, clinical outcomes, cost analysis, readmission patterns

---

## 🔄 Data Pipeline Integration

### Step 1: Analyze Raw Data
```bash
cd scripts
python analyze_data.py
```

**Output:** Comprehensive analysis including:
- Clinical outcomes (recovery, readmission rates)
- Disease distribution patterns
- Cost analysis by condition
- Demographic insights
- Environmental pattern analysis
- Key recommendations

### Step 2: Integrate Datasets
```bash
python integrate_datasets.py
```

**Process:**
1. Loads both hospital datasets
2. Extracts statistics from analysis dataset
3. Maps conditions to unified disease types
4. Enriches with real environmental data (APIs)
5. Generates comprehensive enriched dataset
6. Saves as `final_dataset.csv`

**Output Features:**
- admission_date
- patient_count (aggregated)
- disease_type (unified)
- temperature (from API)
- humidity (from API)
- aqi (from API)
- hospital_area
- source (data lineage)

### Step 3: Preprocess Data
```bash
python preprocess.py
```

**Processing:**
- Handles missing values
- Encodes categorical variables
- Validates data quality
- Creates train/test split
- Prepares for ML model

### Step 4: Train Model
```bash
python train_model.py
```

**Model:**
- RandomForestRegressor
- Features: temperature, humidity, aqi, disease_type, hospital_area
- Target: patient_count
- Evaluation: MAE, RMSE, R² Score

### Step 5: Start API
```bash
cd ../app
python app.py
```

**Endpoints:**
- `/predict` - Predict patient count
- `/recommend` - Medicine recommendations
- `/health` - Status check

---

## 📈 Data Analysis Insights

### From Hospital Analysis Dataset (49 Records)

**Clinical Outcomes:**
- Recovery Rate: ~45%
- Stable Rate: ~35%
- Readmission Rate: ~30%

**Top Conditions (by frequency):**
1. Heart Disease - 7 admissions
2. Diabetes - 6 admissions
3. Stroke - 5 admissions
4. Cancer Types - 5 admissions
5. Appendicitis - 4 admissions

**Cost Analysis:**
- Average Treatment Cost: ₹6,530
- High-Cost Procedures: Surgery, Chemotherapy (₹20,000+)
- Low-Cost Treatments: Injections, Medications (₹100-800)

**Patient Demographics:**
- Average Age: 54 years
- Age Range: 25-78 years
- Gender Distribution: ~50% Male / ~50% Female

**Hospital Stay:**
- Average: 5.5 days
- Range: 1-12 days
- Longest Stays: Cancer patients (9-12 days)

---

## 🔄 Dataset Mapping

### Condition to Disease Type Mapping

| Hospital Condition | ArogyaPredict Disease Type |
|-------------------|--------------------------|
| Heart Disease | Heart Disease |
| Heart Attack | Heart Disease |
| Diabetes | Diabetes |
| Respiratory Infection | Respiratory Infection |
| Hypertension | Hypertension |
| Cancer/Prostate Cancer | Cancer |
| Stroke | Stroke |
| Kidney Stones | Kidney Disease |
| Fractured Arm/Leg | Fractures |
| Appendicitis | Other |
| Childbirth | Other |
| Osteoarthritis | Other |
| Allergic Reaction | Other |

---

## 💾 File Locations

```
ArogyaPredict/
├── data/
│   ├── hospital_base_dataset.csv          [30 records]
│   ├── hospital_analysis_dataset.csv      [49 records]
│   └── final_dataset.csv                  [Generated after integration]
│
├── scripts/
│   ├── analyze_data.py                    [Analysis & insights]
│   ├── integrate_datasets.py              [Dataset integration]
│   ├── fetch_data.py                      [API enrichment]
│   ├── preprocess.py                      [Data preprocessing]
│   └── train_model.py                     [Model training]
```

---

## 📋 Complete Workflow

```bash
# 1. Navigate to project
cd e:\BCA\Final\ArogyaPredict

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env
# Edit .env with your OpenWeather API key

# 4. Analyze datasets
cd scripts
python analyze_data.py

# 5. Integrate datasets
python integrate_datasets.py

# 6. Preprocess data
python preprocess.py

# 7. Train model
python train_model.py

# 8. Start API
cd ../app
python app.py

# 9. Test API (new terminal)
cd ..
python test_api.py
```

---

## 🎯 Key Datasets Characteristics

### Base Dataset Strengths
- ✅ Time-series admission data
- ✅ Medicine usage tracking
- ✅ Hospital area information
- ✅ Direct disease type mapping
- ⚠️ Limited historical period (30 days)

### Analysis Dataset Strengths
- ✅ Rich clinical outcomes
- ✅ Patient demographics
- ✅ Cost information
- ✅ Readmission tracking
- ✅ Satisfaction scores
- ⚠️ No time dimension (cross-sectional)

### Integration Benefits
- ✅ Comprehensive feature set
- ✅ Clinical context + prediction
- ✅ Cost planning insights
- ✅ Outcome tracking
- ✅ Population health insights

---

## 🔍 Analysis Outputs Expected

When running `analyze_data.py`, you'll see:

```
CLINICAL OUTCOMES ANALYSIS
- Outcome Distribution
- Readmission Status
- Patient Satisfaction Score
- Average Hospital Stay

DISEASE DISTRIBUTION ANALYSIS
- Disease frequencies
- Top conditions
- Condition prevalence

COST ANALYSIS
- Average, median, min, max costs
- Cost by condition
- Total treatment costs

DEMOGRAPHIC ANALYSIS
- Age statistics
- Gender distribution
- Gender-disease associations

ENVIRONMENTAL PATTERNS
- Temperature trends
- Humidity levels
- AQI variations
- Patient count correlations

KEY INSIGHTS & RECOMMENDATIONS
- Resource allocation insights
- Follow-up protocol recommendations
- Environmental impact analysis
```

---

## 🚀 Advanced Usage

### Combining Datasets Manually
```python
import pandas as pd

base_df = pd.read_csv("data/hospital_base_dataset.csv")
analysis_df = pd.read_csv("data/hospital_analysis_dataset.csv")

# Merge on condition mapping
combined = pd.merge(base_df, analysis_df, 
                    left_on="disease_type", 
                    right_on="Condition",
                    how="inner")
```

### Custom Analysis
```python
from scripts.analyze_data import HospitalDataAnalyzer

analyzer = HospitalDataAnalyzer()
analyzer.load_datasets()

# Get specific analysis
analyzer.analyze_cost_patterns()
analyzer.analyze_demographics()
```

### Dataset Statistics
```python
# Base dataset
base_records: 30
base_days: 30 unique dates
avg_patients_per_day: 1 patient

# Analysis dataset  
clinical_records: 49 cases
avg_cost: ₹6,530
avg_stay: 5.5 days
readmission_rate: ~30%
```

---

## ⚠️ Data Considerations

### Data Quality
- ✅ No missing values in hospital_base_dataset.csv
- ✅ All required columns present
- ✅ Consistent data types
- ⚠️ Limited temporal coverage in base dataset
- ⚠️ Analysis dataset doesn't have admission dates

### Data Limitations
- Analysis dataset is cross-sectional (no time dimension)
- Base dataset covers short period (30 days)
- No real-time patient flow data
- Sample size is educational (not production-scale)

### Recommendations
- Combine datasets for theoretical analysis
- Use base dataset for time-series predictions
- Use analysis dataset for outcome modeling
- Collect more historical data for production use
- Add real-time admission feeds for live predictions

---

## 📊 Data Lineage

```
Hospital Analysis (49 records)
    ↓ (Extract statistics & patterns)
    
Hospital Base (30 records) + Environmental APIs
    ↓ (integrate_datasets.py)
    
Enriched Dataset (30 records with environmental data)
    ↓ (preprocess.py)
    
Preprocessed Data (encoded, validated)
    ↓ (train_model.py)
    
Trained ML Model + Encoders
    ↓ (app.py)
    
REST API Predictions & Recommendations
```

---

## 🔧 Configuration for Dataset Integration

Edit `config.py` to customize integration:

```python
# Add hospital-specific settings
HOSPITAL_NAME = "Mumbai Central Hospital"
HOSPITAL_LAT = 19.2183
HOSPITAL_LON = 72.9781

# Dataset paths
HOSPITAL_BASE_DATASET = "data/hospital_base_dataset.csv"
HOSPITAL_ANALYSIS_DATASET = "data/hospital_analysis_dataset.csv"
FINAL_DATASET = "data/final_dataset.csv"

# Analysis settings
COST_THRESHOLD = 10000  # High-cost threshold
READMISSION_THRESHOLD = 0.3  # 30% threshold
```

---

## 📝 Troubleshooting

### Issue: "hospital_analysis_dataset.csv not found"
```bash
# Solution: Copy file from e:\BCA\Final\  
copy "..\..\hospital data analysis.csv" data\hospital_analysis_dataset.csv
```

### Issue: Integration fails due to column mismatch
```bash
# Solution: Check column names
python -c "import pandas as pd; print(pd.read_csv('data/hospital_base_dataset.csv').columns)"
python -c "import pandas as pd; print(pd.read_csv('data/hospital_analysis_dataset.csv').columns)"
```

### Issue: API enrichment not working during integration
```bash
# Solution: Check API key in .env
cat .env
# Should have: OPENWEATHER_API_KEY=your_api_key_here
```

---

## 🎓 Learning Resources

- **README.md** - Full system documentation
- **ARCHITECTURE.md** - System design and data flow
- **API_TESTING_EXAMPLES.md** - API usage examples
- **scripts/analyze_data.py** - Data analysis code
- **scripts/integrate_datasets.py** - Integration logic

---

## ✅ Checklist for Data Integration

- [ ] Both CSV files copied to data/ folder
- [ ] API key configured in .env
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Run `analyze_data.py` to verify datasets
- [ ] Run `integrate_datasets.py` to create enriched dataset
- [ ] Verify `final_dataset.csv` was created
- [ ] Run pipeline: preprocess → train → API
- [ ] Test API endpoints with sample data

---

**Data Integration Complete!** 🎉

Your ArogyaPredict system now leverages both hospital datasets for comprehensive patient inflow prediction and analysis.
