# ArogyaPredict - Quick Start Guide

Get up and running with ArogyaPredict in 5 minutes!

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- OpenWeather API key (free from https://openweathermap.org/api)

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies (1 min)

```bash
cd e:\BCA\Final\ArogyaPredict
pip install -r requirements.txt
```

### Step 2: Configure API Key (1 min)

```bash
# Create .env file
copy .env.example .env

# Edit .env and add your OpenWeather API key:
# OPENWEATHER_API_KEY=your_api_key_here
```

Then open `.env` in a text editor and paste your API key.

### Step 3: Prepare Data (1 min each)

Run the complete pipeline with automatic setup:

```bash
# One-command setup with guided steps
python setup.py
```

Or run manually step-by-step:

```bash
# 1. Enrich data with environmental data
cd scripts
python fetch_data.py

# 2. Preprocess the data
python preprocess.py

# 3. Train the model
python train_model.py

# 4. Start the API (go back to main directory)
cd ../app
python app.py
```

### Step 4: Test the API (1 min)

Open another terminal and run:

```bash
cd e:\BCA\Final\ArogyaPredict
python test_api.py
```

## 📊 First Prediction

Once API is running, test it:

**Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 65,
    "aqi": 150
  }'
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
    }
}
```

## 💊 Get Medicine Recommendations

**Request:**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_patient_count": 15,
    "disease_type": "Heart Disease",
    "current_stock": 100
  }'
```

**Response:**
```json
{
    "status": "success",
    "recommendations": [
        {
            "medicine": "Aspirin",
            "current_stock": 100,
            "recommended_quantity": 180,
            "action": "Increase stock",
            "criticality": "NORMAL"
        }
    ]
}
```

## 📁 Project Files Overview

```
ArogyaPredict/
├── data/
│   ├── hospital_base_dataset.csv      # Input data
│   └── final_dataset.csv              # Enriched with environmental data
├── scripts/
│   ├── fetch_data.py                  # Fetch environmental data from APIs
│   ├── preprocess.py                  # Clean and prepare data
│   └── train_model.py                 # Train ML model
├── models/
│   ├── patient_inflow_model.pkl       # Trained model
│   └── encoders.pkl                   # Data encoders
├── app/
│   └── app.py                         # Flask REST API
├── config.py                          # Configuration
├── requirements.txt                   # Dependencies
├── test_api.py                        # API test suite
├── setup.py                           # Automated setup
└── README.md                          # Full documentation
```

## 🔑 API Endpoints

### 1. Health Check
```
GET /health
```
Check if API is running.

### 2. Predict Patient Count
```
POST /predict
```
**Required fields:**
- `temperature` (float): Current temperature in °C
- `humidity` (float): Humidity percentage (0-100)
- `aqi` (float): Air Quality Index

**Optional fields:**
- `disease_type` (str): Type of disease (default: "Heart Disease")
- `hospital_area` (str): Hospital area (default: "General Ward")

**Returns:** Predicted patient count with confidence range

### 3. Medicine Recommendations
```
POST /recommend
```
**Required fields:**
- `predicted_patient_count` (float): Predicted number of patients
- `disease_type` (str): Type of disease

**Optional fields:**
- `current_stock` (int): Current medicine stock (default: 100)

**Returns:** List of medicine recommendations with actions

## 🐛 Troubleshooting

### Issue: "Model not found" error

**Solution:** Run the training pipeline first:
```bash
cd scripts
python train_model.py
```

### Issue: "API key not found" error

**Solution:** Make sure .env file has your OpenWeather API key:
```bash
# Check .env file
cat .env
```

And get a free key from https://openweathermap.org/api

### Issue: "Module not found" error

**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: API won't start

**Solution:** Make sure port 5000 is not in use:
```bash
# Change port in app/app.py if necessary
# Change last line from: app.run(host="0.0.0.0", port=5000)
# To: app.run(host="0.0.0.0", port=5001)
```

## 📚 Next Steps

1. **Read Full Documentation:**
   ```bash
   cat README.md
   ```

2. **Explore the Code:**
   - `config.py` - All configuration options
   - `scripts/fetch_data.py` - Data enrichment logic
   - `app/app.py` - API endpoints

3. **Customize:**
   - Add more diseases to `config.py`
   - Modify model hyperparameters in `config.py`
   - Add more medicine types to `MEDICINE_DATABASE`

4. **Deploy:**
   - Use Gunicorn for production: `pip install gunicorn`
   - Run: `gunicorn -w 4 -b 0.0.0.0:5000 app.app:app`

## 💡 Example Workflow

```bash
# 1. Navigate to project
cd e:\BCA\Final\ArogyaPredict

# 2. Install packages
pip install -r requirements.txt

# 3. Setup .env with API key
copy .env.example .env
# Edit .env file with your API key

# 4. Run full pipeline
python scripts/fetch_data.py
python scripts/preprocess.py
python scripts/train_model.py

# 5. Start API in one terminal
python app/app.py

# 6. Test API in another terminal
python test_api.py

# 7. Make curl requests
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 30, "humidity": 70, "aqi": 160}'
```

## 🎯 Key Features

✅ **Real Environmental Data** - Uses OpenAQ API for AQI, OpenWeather API for weather  
✅ **Production-Ready** - Error handling, logging, input validation  
✅ **Modular Architecture** - Separate modules for each step  
✅ **Easy Deployment** - Flask REST API, easily containerizable  
✅ **Medicine Recommendations** - Smart stock planning based on predictions  
✅ **Comprehensive Testing** - Built-in test suite  

## 📞 Support

For issues:
1. Check the error message in terminal
2. Review the code comments
3. Check README.md for detailed documentation
4. Check the logs in each script

## 🎓 Learning Paths

**Beginner:**
- Run test_api.py to understand API usage
- Review config.py to see all options
- Try different input parameters in curl requests

**Intermediate:**
- Read through the Python scripts
- Modify hyperparameters in config.py
- Test with custom data

**Advanced:**
- Add new disease types to medicine database
- Implement additional environmental factors
- Deploy using Docker/Kubernetes

---

**Happy Predicting! 🚀**

For full details, see [README.md](README.md)
