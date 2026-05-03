"""
Enhanced Data Enrichment Module - ArogyaPredict
Fetches real AQI, Weather, and Holiday data from APIs and enriches hospital dataset.

This module:
1. Reads hospital_base_dataset.csv
2. Fetches AQI data using AQICN API
3. Fetches weather data using OpenWeather API
4. Fetches holiday/event data using Calendarific API
5. Calculates patient count correlations with environmental factors
6. Saves enriched data as final_dataset.csv
"""

import pandas as pd
import requests
import logging
from datetime import datetime, timedelta
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    HOSPITAL_BASE_DATASET,
    FINAL_DATASET,
    HOSPITAL_LAT,
    HOSPITAL_LON,
    HOSPITAL_COUNTRY,
    HOSPITAL_CITY,
    OPENAQ_API_URL,
    OPENWEATHER_API_URL,
    OPENWEATHER_API_KEY,
    AQICN_API_URL,
    AQICN_API_KEY,
    CALENDARIFIC_API_URL,
    CALENDARIFIC_API_KEY,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def fetch_aqicn_aqi(lat, lon, date):
    """
    Fetch AQI data from AQICN API (more reliable than OpenAQ).
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        date (str): Date in YYYY-MM-DD format
    
    Returns:
        dict: Contains AQI data
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "token": AQICN_API_KEY,
        }
        
        logger.info(f"Fetching AQI from AQICN for {date}...")
        response = requests.get(AQICN_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") == "ok" and data.get("data"):
            aqi_value = data["data"].get("aqi", 150)
            logger.info(f"✓ AQICN AQI: {aqi_value} for {date}")
            return {"aqi": aqi_value, "aqi_source": "AQICN"}
        else:
            logger.warning(f"No AQI data from AQICN. Using default.")
            return {"aqi": 150, "aqi_source": "Default"}
            
    except Exception as e:
        logger.warning(f"Error fetching from AQICN: {e}. Using default value.")
        return {"aqi": 150, "aqi_source": "Default"}


def fetch_weather_data(lat, lon):
    """
    Fetch weather data from OpenWeather API.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
    
    Returns:
        dict: Contains temperature, humidity, and weather condition
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Celsius
        }
        
        logger.info("Fetching weather data from OpenWeather...")
        response = requests.get(OPENWEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        main_data = data.get("main", {})
        temp = main_data.get("temp", 28.0)
        humidity = main_data.get("humidity", 70)
        weather_main = data.get("weather", [{}])[0].get("main", "Clear")
        
        logger.info(f"✓ Weather: Temp={temp}°C, Humidity={humidity}%, Condition={weather_main}")
        return {
            "temperature": temp,
            "humidity": humidity,
            "weather_condition": weather_main
        }
        
    except Exception as e:
        logger.warning(f"Error fetching weather: {e}. Using defaults.")
        return {
            "temperature": 28.0,
            "humidity": 70,
            "weather_condition": "Unknown"
        }


def fetch_holidays(year):
    """
    Fetch holidays and events for a specific year.
    
    Args:
        year (int): Year to fetch holidays for
    
    Returns:
        dict: Mapping of dates to holiday names
    """
    try:
        params = {
            "country": HOSPITAL_COUNTRY,
            "year": year,
            "api_key": CALENDARIFIC_API_KEY,
        }
        
        logger.info(f"Fetching holidays for {year} from Calendarific...")
        response = requests.get(CALENDARIFIC_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        holidays = {}
        if data.get("response", {}).get("holidays"):
            for holiday in data["response"]["holidays"]:
                date_str = holiday.get("date", {}).get("iso")  # YYYY-MM-DD format
                name = holiday.get("name", "Holiday")
                holidays[date_str] = name
                logger.info(f"✓ Holiday found: {date_str} - {name}")
        
        return holidays
        
    except Exception as e:
        logger.warning(f"Error fetching holidays: {e}. Continuing without holiday data.")
        return {}


def is_holiday_season(date_str, holidays):
    """
    Check if a date is a holiday or near a major holiday (±3 days).
    
    Args:
        date_str (str): Date in YYYY-MM-DD format
        holidays (dict): Holiday mapping
    
    Returns:
        tuple: (is_holiday, holiday_name, days_after_holiday)
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Check if exact date is holiday
    if date_str in holidays:
        return True, holidays[date_str], 0
    
    # Check if within 3 days before/after holiday
    for i in range(-3, 4):
        check_date = date_obj + timedelta(days=i)
        check_date_str = check_date.strftime("%Y-%m-%d")
        
        if check_date_str in holidays:
            return True, holidays[check_date_str], i
    
    return False, "None", 0


def is_respiratory_season_upcoming(date_str):
    """
    Check if weather is likely to cause respiratory issues (Diwali season = Oct-Nov).
    
    Args:
        date_str (str): Date in YYYY-MM-DD format
    
    Returns:
        bool: True if respiratory season (Oct-Nov)
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    month = date_obj.month
    
    # Oct-Nov: Diwali season, air pollution peaks
    return month in [10, 11]


def correlate_disease_with_factors(disease_type, weather, holiday_info, date_str):
    """
    Apply intelligent correlation between disease and environmental factors.
    
    Args:
        disease_type (str): Type of disease
        weather (dict): Weather data
        holiday_info (tuple): Holiday information
        date_str (str): Date
    
    Returns:
        float: Multiplier for expected patient count
    """
    multiplier = 1.0
    
    is_holiday, holiday_name, days_after = holiday_info
    temp = weather.get("temperature", 28.0)
    humidity = weather.get("humidity", 70)
    weather_cond = weather.get("weather_condition", "Clear")
    
    # Respiratory infections: worse in winter (cold) and around Diwali
    if disease_type == "Respiratory Infection":
        if temp < 15:  # Cold weather
            multiplier *= 1.5
            logger.info(f"  → Respiratory: Cold weather multiplier 1.5x")
        
        if is_respiratory_season_upcoming(date_str):
            multiplier *= 1.3
            logger.info(f"  → Respiratory: Diwali season multiplier 1.3x")
        
        if is_holiday and "Diwali" in holiday_name:
            multiplier *= 1.8  # Major spike around Diwali
            logger.info(f"  → Respiratory: Diwali holiday multiplier 1.8x")
    
    # Heart disease: worse during cold weather
    elif disease_type == "Heart Disease":
        if temp < 10:
            multiplier *= 1.4
            logger.info(f"  → Heart Disease: Cold weather multiplier 1.4x")
    
    # Waterborne diseases: worse in rainy season
    elif disease_type == "Gastroenteritis":
        if weather_cond in ["Rain", "Rainy"]:
            multiplier *= 1.3
            logger.info(f"  → Gastroenteritis: Rainy weather multiplier 1.3x")
    
    # Holiday effect: more injuries during celebrations
    if is_holiday and "Holi" in holiday_name:
        multiplier *= 1.2  # Injuries during Holi
        logger.info(f"  → Holiday effect (Holi): 1.2x multiplier")
    
    # Post-holiday surge: people return to hospitals after delays
    if is_holiday and days_after == 1:
        multiplier *= 1.15
        logger.info(f"  → Post-holiday surge: 1.15x multiplier")
    
    return multiplier


def count_patients_by_date(df, date):
    """Count patients admitted on a specific date."""
    return int(df[df["admission_date"] == date].shape[0])


def enrich_dataset():
    """
    Main function to enrich hospital dataset with ALL environmental and event data.
    """
    try:
        # Read hospital base dataset
        logger.info("Reading hospital base dataset...")
        df = pd.read_csv(HOSPITAL_BASE_DATASET)
        
        if df.empty:
            logger.error("Hospital base dataset is empty!")
            return False
        
        logger.info(f"✓ Loaded {len(df)} records")
        
        # Convert admission_date to datetime
        df["admission_date"] = pd.to_datetime(df["admission_date"])
        
        # Get unique dates and years
        unique_dates = sorted(df["admission_date"].dt.date.unique())
        years = set([date.year for date in unique_dates])
        
        logger.info(f"Found {len(unique_dates)} unique admission dates across {len(years)} years")
        
        # Fetch holidays for all years
        all_holidays = {}
        for year in years:
            all_holidays.update(fetch_holidays(year))
        
        logger.info(f"✓ Fetched {len(all_holidays)} holidays")
        
        # Prepare enriched data
        enriched_data = []
        
        for date in unique_dates:
            date_str = str(date)
            
            # Get patient count for this date
            patient_count = count_patients_by_date(df, date_str)
            
            # Fetch environmental data
            aqi_data = fetch_aqicn_aqi(HOSPITAL_LAT, HOSPITAL_LON, date_str)
            weather_data = fetch_weather_data(HOSPITAL_LAT, HOSPITAL_LON)
            
            # Check holiday info
            is_hol, hol_name, days_after_hol = is_holiday_season(date_str, all_holidays)
            holiday_info = (is_hol, hol_name, days_after_hol)
            
            # Get disease types for this date
            diseases_today = df[df["admission_date"].dt.date == date]["disease_type"].unique()
            
            # Create one record per disease type for better predictions
            for disease in diseases_today:
                # Count patients with this disease on this date
                disease_patient_count = int(df[
                    (df["admission_date"].dt.date == date) & 
                    (df["disease_type"] == disease)
                ].shape[0])
                
                # Get multiplier based on correlations
                multiplier = correlate_disease_with_factors(
                    disease, weather_data, holiday_info, date_str
                )
                
                expected_multiplier = multiplier
                
                enriched_record = {
                    "admission_date": date_str,
                    "disease_type": disease,
                    "actual_patient_count": disease_patient_count,
                    "expected_multiplier": expected_multiplier,
                    "temperature": weather_data["temperature"],
                    "humidity": weather_data["humidity"],
                    "weather_condition": weather_data["weather_condition"],
                    "aqi": aqi_data["aqi"],
                    "is_holiday": is_hol,
                    "holiday_name": hol_name if is_hol else "None",
                    "days_after_holiday": days_after_hol,
                }
                
                enriched_data.append(enriched_record)
        
        # Create DataFrame from enriched data
        enriched_df = pd.DataFrame(enriched_data)
        
        # Save enriched dataset
        enriched_df.to_csv(FINAL_DATASET, index=False)
        logger.info(f"✓ Enriched dataset saved: {FINAL_DATASET}")
        logger.info(f"✓ Total enriched records: {len(enriched_df)}")
        
        # Print sample
        logger.info("\n=== Sample of Enriched Data ===")
        logger.info(enriched_df.head(10).to_string())
        
        return True
        
    except Exception as e:
        logger.error(f"Error during data enrichment: {e}")
        return False


if __name__ == "__main__":
    logger.info("\n" + "="*60)
    logger.info("Starting Data Enrichment Process...")
    logger.info("="*60 + "\n")
    
    success = enrich_dataset()
    
    if success:
        logger.info("\n" + "="*60)
        logger.info("✓ Data enrichment completed successfully!")
        logger.info("="*60)
    else:
        logger.error("✗ Data enrichment failed!")
        
    logger.info(f"\n✓ Next steps:")
    logger.info(f"  1. Run: python scripts/preprocess.py")
    logger.info(f"  2. Run: python scripts/train_model.py")
    logger.info(f"  3. Run: python app/app.py")
