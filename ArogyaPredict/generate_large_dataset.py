"""
Generate large realistic hospital dataset for ArogyaPredict
Creates 1500+ records with realistic variations for a large hospital organization
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("\n" + "="*70)
print("GENERATING LARGE REALISTIC HOSPITAL DATASET")
print("="*70)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_RECORDS = 1500
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Disease types and their characteristics
diseases = {
    "Heart Disease": {"base_patients": 3.5, "temp_sensitivity": 0.15},
    "Diabetes": {"base_patients": 2.8, "temp_sensitivity": 0.08},
    "Respiratory Infection": {"base_patients": 4.2, "temp_sensitivity": 0.25},
    "Hypertension": {"base_patients": 2.5, "temp_sensitivity": 0.10},
    "Kidney Disease": {"base_patients": 1.8, "temp_sensitivity": 0.05},
    "Gastroenteritis": {"base_patients": 2.2, "temp_sensitivity": 0.12},
    "Pediatric Illness": {"base_patients": 3.0, "temp_sensitivity": 0.18},
    "Malaria": {"base_patients": 1.5, "temp_sensitivity": 0.20},
}

# Weather conditions
weather_conditions = ["Clear", "Haze", "Smoke", "Rain", "Cloudy", "Sunny", "Rainy"]

# Indian holidays
holidays = {
    "New Year's Day": (1, 1),
    "Lohri": (1, 13),
    "Makar Sankranti": (1, 14),
    "Pongal": (1, 14),
    "Holi": (3, 25),
    "Diwali": (11, 1),
    "Christmas": (12, 25),
}

def is_holiday(date):
    """Check if date is a holiday"""
    for holiday_name, (month, day) in holidays.items():
        if date.month == month and date.day == day:
            return True, holiday_name
    return False, "None"

def get_weather_for_date(date):
    """Get weather condition based on date (seasonal patterns)"""
    month = date.month
    
    if month in [6, 7, 8, 9]:  # Monsoon
        weather_weights = [0.1, 0.15, 0.05, 0.5, 0.15, 0.05, 0.0]
    elif month in [10, 11, 1, 2, 3]:  # Winter/Spring
        weather_weights = [0.2, 0.35, 0.1, 0.05, 0.2, 0.1, 0.0]
    else:  # Summer
        weather_weights = [0.05, 0.4, 0.15, 0.1, 0.1, 0.2, 0.0]
    
    return np.random.choice(weather_conditions, p=weather_weights)

def get_temperature_for_month(month):
    """Get realistic temperature based on month"""
    # India's temperature patterns
    month_temps = {
        1: 25, 2: 28, 3: 32, 4: 35, 5: 35, 6: 32,
        7: 28, 8: 27, 9: 28, 10: 30, 11: 28, 12: 25
    }
    base_temp = month_temps.get(month, 28)
    variation = np.random.normal(0, 3)
    return round(base_temp + variation, 2)

def get_humidity_for_weather(weather):
    """Get realistic humidity based on weather"""
    humidity_ranges = {
        "Clear": (35, 55),
        "Haze": (50, 70),
        "Smoke": (30, 50),
        "Rain": (75, 95),
        "Cloudy": (60, 80),
        "Sunny": (20, 45),
        "Rainy": (70, 90),
    }
    min_h, max_h = humidity_ranges.get(weather, (40, 70))
    return round(np.random.uniform(min_h, max_h), 2)

def get_aqi_for_weather(weather):
    """Get realistic AQI based on weather"""
    aqi_ranges = {
        "Clear": (50, 100),
        "Haze": (150, 250),
        "Smoke": (200, 350),
        "Rain": (30, 80),
        "Cloudy": (80, 150),
        "Sunny": (40, 90),
        "Rainy": (20, 70),
    }
    min_aqi, max_aqi = aqi_ranges.get(weather, (100, 150))
    return int(np.random.uniform(min_aqi, max_aqi))

def calculate_patient_count(disease, temperature, humidity, aqi, is_holiday, days_after_holiday):
    """Calculate realistic patient count based on multiple factors"""
    
    disease_info = diseases[disease]
    base_count = disease_info["base_patients"]
    
    # Temperature impact
    temp_sensitivity = disease_info["temp_sensitivity"]
    temp_impact = 1 + (temperature - 28) * temp_sensitivity / 10  # Reference temp = 28°C
    
    # Humidity impact (high humidity increases most diseases)
    humidity_impact = 1 + (humidity - 60) * 0.005
    
    # AQI impact (high pollution)
    aqi_impact = 1 + max(0, (aqi - 100)) * 0.002
    
    # Holiday effect (usually decreases)
    holiday_multiplier = 0.7 if is_holiday else 1.0
    if days_after_holiday < 0:  # Days before holiday
        holiday_multiplier = 1.1
    elif days_after_holiday < 3 and days_after_holiday >= 0:  # Just after holiday
        holiday_multiplier = 0.8
    
    # Random variation (±30%)
    random_factor = np.random.uniform(0.7, 1.3)
    
    # Final calculation
    predicted_count = base_count * temp_impact * humidity_impact * aqi_impact * holiday_multiplier * random_factor
    
    return max(1, int(round(predicted_count)))

# Generate records
print(f"\nGenerating {NUM_RECORDS} records from {START_DATE.date()} to {END_DATE.date()}...")
print("This may take a minute...\n")

records = []
current_date = START_DATE

# Generate one record per disease per day (roughly)
days_in_range = (END_DATE - START_DATE).days
diseases_list = list(diseases.keys())

for i in range(NUM_RECORDS):
    # Randomly distribute dates
    days_offset = np.random.randint(0, days_in_range)
    admission_date = START_DATE + timedelta(days=days_offset)
    
    # Select disease
    disease_type = np.random.choice(diseases_list)
    
    # Get weather for that date
    weather = get_weather_for_date(admission_date)
    
    # Get environmental conditions
    temperature = get_temperature_for_month(admission_date.month)
    humidity = get_humidity_for_weather(weather)
    aqi = get_aqi_for_weather(weather)
    
    # Check if holiday
    is_hol, holiday_name = is_holiday(admission_date)
    is_holiday_int = 1 if is_hol else 0
    
    # Calculate days after holiday (for holiday effect)
    days_after = 0
    if not is_hol:
        for hol_date in holidays.values():
            hol_datetime = datetime(admission_date.year, hol_date[0], hol_date[1])
            days_diff = (admission_date - hol_datetime).days
            if 0 <= days_diff <= 7:
                days_after = days_diff
                break
    
    expected_multiplier = 1.0 + np.random.uniform(-0.2, 0.2)
    expected_multiplier = round(expected_multiplier, 2)
    
    # Calculate patient count
    actual_patient_count = calculate_patient_count(
        disease_type, temperature, humidity, aqi, 
        is_holiday_int, days_after
    )
    
    records.append({
        "admission_date": admission_date.date(),
        "disease_type": disease_type,
        "actual_patient_count": actual_patient_count,
        "expected_multiplier": expected_multiplier,
        "temperature": temperature,
        "humidity": humidity,
        "weather_condition": weather,
        "aqi": aqi,
        "is_holiday": is_hol,
        "holiday_name": holiday_name,
        "days_after_holiday": days_after,
    })

# Create DataFrame
df = pd.DataFrame(records)

# Sort by date
df = df.sort_values('admission_date').reset_index(drop=True)

# Save to CSV
output_path = "data/final_dataset.csv"
df.to_csv(output_path, index=False)

print(f"✅ Dataset generated successfully!")
print(f"   File: {output_path}")
print(f"   Records: {len(df)}")
print(f"   Date Range: {df['admission_date'].min()} to {df['admission_date'].max()}")
print(f"\n📊 Dataset Statistics:")
print(f"   Total Records: {len(df)}")
print(f"   Disease Types: {df['disease_type'].nunique()}")
print(f"   Temperature Range: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C")
print(f"   Humidity Range: {df['humidity'].min():.1f}% to {df['humidity'].max():.1f}%")
print(f"   AQI Range: {df['aqi'].min()} to {df['aqi'].max()}")
print(f"   Avg Patients/Day: {df['actual_patient_count'].mean():.1f}")
print(f"   Max Patients/Day: {df['actual_patient_count'].max()}")
print(f"   Holidays in Dataset: {df['is_holiday'].sum()}")

print(f"\n📋 Disease Distribution:")
disease_counts = df['disease_type'].value_counts()
for disease, count in disease_counts.items():
    percentage = (count / len(df)) * 100
    print(f"   {disease}: {count} records ({percentage:.1f}%)")

print("\n" + "="*70)
print("✅ Now run: python scripts/train_model.py")
print("="*70 + "\n")
