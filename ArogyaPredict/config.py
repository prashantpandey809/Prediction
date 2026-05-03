"""
Configuration module for ArogyaPredict project.
Contains API keys, paths, and constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAQ_API_URL = "https://api.openaq.org/v2/latest"
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
AQICN_API_URL = "https://api.waqi.info/feed/geo"
CALENDARIFIC_API_URL = "https://www.calendarific.com/api/v2/holidays"

# API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_openweather_api_key_here")
AQICN_API_KEY = os.getenv("AQICN_API_KEY", "your_aqicn_api_key_here")
CALENDARIFIC_API_KEY = os.getenv("CALENDARIFIC_API_KEY", "your_calendarific_api_key_here")

# Coordinates for hospital location (Mumbai, India)
HOSPITAL_LAT = float(os.getenv("HOSPITAL_LAT", "19.2183"))
HOSPITAL_LON = float(os.getenv("HOSPITAL_LON", "72.9781"))
HOSPITAL_COUNTRY = os.getenv("HOSPITAL_COUNTRY", "IN")
HOSPITAL_STATE = "Maharashtra"
HOSPITAL_CITY = "Mumbai"

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

HOSPITAL_BASE_DATASET = os.path.join(DATA_DIR, "hospital_base_dataset.csv")
FINAL_DATASET = os.path.join(DATA_DIR, "final_dataset.csv")
MODEL_PATH = os.path.join(MODELS_DIR, "patient_inflow_model.pkl")
ENCODER_PATH = os.path.join(MODELS_DIR, "encoders.pkl")

# Model Configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42
N_ESTIMATORS = 100
MAX_DEPTH = 15
MIN_SAMPLES_SPLIT = 5
MIN_SAMPLES_LEAF = 2

# Medicine Stock Thresholds
LOW_STOCK_THRESHOLD = 50
CRITICAL_STOCK_THRESHOLD = 20
STOCK_INCREASE_PERCENT = 20
STOCK_DECREASE_PERCENT = 10

# Disease Types
DISEASE_TYPES = [
    "Heart Disease",
    "Diabetes",
    "Respiratory Infection",
    "Hypertension",
    "Cancer",
    "Kidney Disease",
    "Gastroenteritis",
    "Fractures",
    "Stroke",
    "Other"
]

# Hospital Areas
HOSPITAL_AREAS = ["ICU", "General Ward", "Emergency", "OPD", "Pediatrics"]

# Medicine Database (Disease -> Medicines mapping) - EXPANDED & COMPREHENSIVE
MEDICINE_DATABASE = {
    "Heart Disease": [
        {"name": "Aspirin", "base_qty": 200, "expiry_critical_days": 30, "dosage": "100mg", "form": "Tablet"},
        {"name": "Atorvastatin", "base_qty": 150, "expiry_critical_days": 60, "dosage": "20mg", "form": "Tablet"},
        {"name": "Lisinopril", "base_qty": 150, "expiry_critical_days": 60, "dosage": "10mg", "form": "Tablet"},
        {"name": "Metoprolol", "base_qty": 120, "expiry_critical_days": 60, "dosage": "50mg", "form": "Tablet"},
        {"name": "Nitroglycerin", "base_qty": 80, "expiry_critical_days": 30, "dosage": "0.6mg", "form": "Sublingual Tablet"},
        {"name": "Clopidogrel", "base_qty": 100, "expiry_critical_days": 90, "dosage": "75mg", "form": "Tablet"},
    ],
    "Diabetes": [
        {"name": "Insulin Glargine", "base_qty": 250, "expiry_critical_days": 7, "dosage": "100IU/ml", "form": "Injection"},
        {"name": "Metformin", "base_qty": 300, "expiry_critical_days": 90, "dosage": "500mg", "form": "Tablet"},
        {"name": "Glipizide", "base_qty": 200, "expiry_critical_days": 90, "dosage": "10mg", "form": "Tablet"},
        {"name": "Sitagliptin", "base_qty": 150, "expiry_critical_days": 90, "dosage": "100mg", "form": "Tablet"},
        {"name": "Pioglitazone", "base_qty": 120, "expiry_critical_days": 90, "dosage": "30mg", "form": "Tablet"},
        {"name": "Acarbose", "base_qty": 180, "expiry_critical_days": 90, "dosage": "100mg", "form": "Tablet"},
        {"name": "Exenatide", "base_qty": 100, "expiry_critical_days": 30, "dosage": "10mcg", "form": "Injection Pen"},
    ],
    "Respiratory Infection": [
        {"name": "Amoxicillin", "base_qty": 300, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
        {"name": "Azithromycin", "base_qty": 250, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
        {"name": "Salbutamol", "base_qty": 200, "expiry_critical_days": 90, "dosage": "100mcg", "form": "Inhaler"},
        {"name": "Omeprazole", "base_qty": 180, "expiry_critical_days": 90, "dosage": "20mg", "form": "Capsule"},
        {"name": "Levofloxacin", "base_qty": 150, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
        {"name": "Fluticasone", "base_qty": 120, "expiry_critical_days": 90, "dosage": "50mcg", "form": "Nasal Spray"},
        {"name": "Montelukast", "base_qty": 140, "expiry_critical_days": 90, "dosage": "10mg", "form": "Tablet"},
        {"name": "Paracetamol", "base_qty": 400, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
    ],
    "Hypertension": [
        {"name": "Amlodipine", "base_qty": 250, "expiry_critical_days": 90, "dosage": "5mg", "form": "Tablet"},
        {"name": "Atenolol", "base_qty": 200, "expiry_critical_days": 90, "dosage": "50mg", "form": "Tablet"},
        {"name": "Losartan", "base_qty": 200, "expiry_critical_days": 90, "dosage": "50mg", "form": "Tablet"},
        {"name": "Enalapril", "base_qty": 180, "expiry_critical_days": 90, "dosage": "10mg", "form": "Tablet"},
        {"name": "Hydrochlorothiazide", "base_qty": 160, "expiry_critical_days": 90, "dosage": "25mg", "form": "Tablet"},
        {"name": "Valsartan", "base_qty": 150, "expiry_critical_days": 90, "dosage": "80mg", "form": "Tablet"},
    ],
    "Cancer": [
        {"name": "Cisplatin", "base_qty": 50, "expiry_critical_days": 7, "dosage": "50mg", "form": "Solution"},
        {"name": "Methotrexate", "base_qty": 80, "expiry_critical_days": 30, "dosage": "25mg", "form": "Injection"},
        {"name": "Doxorubicin", "base_qty": 60, "expiry_critical_days": 7, "dosage": "10mg/ml", "form": "Solution"},
        {"name": "Paclitaxel", "base_qty": 40, "expiry_critical_days": 7, "dosage": "6mg/ml", "form": "Infusion"},
        {"name": "Tamoxifen", "base_qty": 120, "expiry_critical_days": 90, "dosage": "20mg", "form": "Tablet"},
    ],
    "Kidney Disease": [
        {"name": "Furosemide", "base_qty": 200, "expiry_critical_days": 60, "dosage": "40mg", "form": "Tablet"},
        {"name": "Potassium Supplement", "base_qty": 150, "expiry_critical_days": 90, "dosage": "20mEq", "form": "Tablet"},
        {"name": "Calcium Carbonate", "base_qty": 180, "expiry_critical_days": 90, "dosage": "500mg", "form": "Tablet"},
        {"name": "Phosphate Binder", "base_qty": 140, "expiry_critical_days": 60, "dosage": "1g", "form": "Tablet"},
        {"name": "Erythropoietin", "base_qty": 100, "expiry_critical_days": 7, "dosage": "2000IU", "form": "Injection"},
    ],
    "Gastroenteritis": [
        {"name": "Metoclopramide", "base_qty": 200, "expiry_critical_days": 60, "dosage": "10mg", "form": "Tablet"},
        {"name": "Ondansetron", "base_qty": 180, "expiry_critical_days": 60, "dosage": "4mg", "form": "Tablet"},
        {"name": "Loperamide", "base_qty": 150, "expiry_critical_days": 90, "dosage": "2mg", "form": "Tablet"},
        {"name": "Ciprofloxacin", "base_qty": 160, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
        {"name": "Electrolyte Solution", "base_qty": 300, "expiry_critical_days": 30, "dosage": "Mix", "form": "Powder"},
        {"name": "Bismuth Subsalicylate", "base_qty": 140, "expiry_critical_days": 90, "dosage": "262mg", "form": "Tablet"},
    ],
    "Fractures": [
        {"name": "Ibuprofen", "base_qty": 300, "expiry_critical_days": 60, "dosage": "400mg", "form": "Tablet"},
        {"name": "Paracetamol", "base_qty": 350, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
        {"name": "Tramadol", "base_qty": 160, "expiry_critical_days": 90, "dosage": "50mg", "form": "Tablet"},
        {"name": "Calcium Supplement", "base_qty": 200, "expiry_critical_days": 90, "dosage": "1000mg", "form": "Tablet"},
        {"name": "Vitamin D", "base_qty": 180, "expiry_critical_days": 90, "dosage": "1000IU", "form": "Capsule"},
        {"name": "Tetanus Toxoid", "base_qty": 100, "expiry_critical_days": 14, "dosage": "0.5ml", "form": "Injection"},
    ],
    "Stroke": [
        {"name": "Aspirin", "base_qty": 250, "expiry_critical_days": 30, "dosage": "100mg", "form": "Tablet"},
        {"name": "Ticlopidine", "base_qty": 180, "expiry_critical_days": 90, "dosage": "250mg", "form": "Tablet"},
        {"name": "Alteplase", "base_qty": 30, "expiry_critical_days": 3, "dosage": "100mg", "form": "Solution"},
        {"name": "Atorvastatin", "base_qty": 200, "expiry_critical_days": 60, "dosage": "40mg", "form": "Tablet"},
        {"name": "Lisinopril", "base_qty": 160, "expiry_critical_days": 60, "dosage": "10mg", "form": "Tablet"},
    ],
    "Respiratory Infection": [
        {"name": "Ceftriaxone", "base_qty": 200, "expiry_critical_days": 30, "dosage": "1g", "form": "Vial"},
        {"name": "Clarithromycin", "base_qty": 140, "expiry_critical_days": 60, "dosage": "500mg", "form": "Tablet"},
    ],
    "Other": [
        {"name": "Antihistamine", "base_qty": 150, "expiry_critical_days": 90, "dosage": "10mg", "form": "Tablet"},
        {"name": "Iodine Solution", "base_qty": 100, "expiry_critical_days": 60, "dosage": "5%", "form": "Solution"},
        {"name": "Bandages", "base_qty": 500, "expiry_critical_days": 365, "dosage": "Various", "form": "Roll"},
        {"name": "Saline Solution", "base_qty": 400, "expiry_critical_days": 90, "dosage": "0.9%", "form": "Bottle"},
        {"name": "Antiseptic Wipes", "base_qty": 600, "expiry_critical_days": 180, "dosage": "Pack", "form": "Wipe"},
    ]
}

print("[OK] Configuration loaded successfully")
