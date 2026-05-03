"""
Enhanced Data Integration Module - ArogyaPredict
Integrates multiple hospital datasets and enhances with environmental data.

This module:
1. Combines hospital_base_dataset.csv with hospital_analysis_dataset.csv
2. Handles different data formats and structures
3. Extracts admission patterns from rich hospital data
4. Enriches with environmental data from APIs
5. Generates comprehensive enriched dataset
"""

import pandas as pd
import numpy as np
import requests
import logging
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    HOSPITAL_BASE_DATASET,
    FINAL_DATASET,
    HOSPITAL_LAT,
    HOSPITAL_LON,
    OPENAQ_API_URL,
    OPENWEATHER_API_URL,
    OPENWEATHER_API_KEY,
    DATA_DIR,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_hospital_analysis_dataset():
    """
    Load the hospital analysis dataset with rich clinical data.
    
    Returns:
        pd.DataFrame: Hospital analysis dataset with patient details
    """
    analysis_file = os.path.join(DATA_DIR, "hospital_analysis_dataset.csv")
    
    try:
        logger.info(f"Loading hospital analysis dataset from {analysis_file}...")
        df = pd.read_csv(analysis_file)
        logger.info(f"✓ Loaded {len(df)} records from analysis dataset")
        logger.info(f"  Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        logger.warning(f"Hospital analysis dataset not found at {analysis_file}")
        return None
    except Exception as e:
        logger.error(f"Error loading hospital analysis dataset: {e}")
        return None


def map_condition_to_disease_type(condition):
    """
    Map hospital condition to disease type for consistency.
    
    Args:
        condition (str): Hospital condition name
        
    Returns:
        str: Mapped disease type
    """
    condition_mapping = {
        "Heart Disease": "Heart Disease",
        "Heart Attack": "Heart Disease",
        "Diabetes": "Diabetes",
        "Respiratory Infection": "Respiratory Infection",
        "Hypertension": "Hypertension",
        "Cancer": "Cancer",
        "Prostate Cancer": "Cancer",
        "Stroke": "Stroke",
        "Kidney Stones": "Kidney Disease",
        "Fractured Arm": "Fractures",
        "Fractured Leg": "Fractures",
        "Appendicitis": "Other",
        "Childbirth": "Other",
        "Osteoarthritis": "Other",
        "Allergic Reaction": "Other",
    }
    
    return condition_mapping.get(condition, "Other")


def extract_admission_patterns(analysis_df):
    """
    Extract admission patterns and statistics from analysis dataset.
    
    Args:
        analysis_df (pd.DataFrame): Hospital analysis dataset
        
    Returns:
        dict: Aggregated statistics
    """
    stats = {
        "total_admissions": len(analysis_df),
        "by_condition": analysis_df["Condition"].value_counts().to_dict() if "Condition" in analysis_df.columns else {},
        "average_stay": analysis_df["Length_of_Stay"].mean() if "Length_of_Stay" in analysis_df.columns else 0,
        "readmission_rate": (analysis_df["Readmission"].value_counts().get("Yes", 0) / len(analysis_df) * 100) if "Readmission" in analysis_df.columns else 0,
        "satisfaction_score": analysis_df["Satisfaction"].mean() if "Satisfaction" in analysis_df.columns else 0,
    }
    
    logger.info(f"Analysis Dataset Statistics:")
    logger.info(f"  Total Admissions: {stats['total_admissions']}")
    logger.info(f"  Average Stay: {stats['average_stay']:.1f} days")
    logger.info(f"  Readmission Rate: {stats['readmission_rate']:.1f}%")
    logger.info(f"  Satisfaction Score: {stats['satisfaction_score']:.2f}/5")
    
    return stats


def fetch_aqi_data(lat, lon, date):
    """Fetch AQI data from OpenAQ API."""
    try:
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": 10000,
            "limit": 1,
        }
        
        response = requests.get(OPENAQ_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("results") and len(data["results"]) > 0:
            result = data["results"][0]
            aqi_value = result.get("measurements", [{}])[0].get("value", None)
            
            if aqi_value is None:
                aqi_value = 150
                
            logger.debug(f"✓ AQI data fetched: {aqi_value} for {date}")
            return aqi_value
        else:
            logger.debug(f"No AQI data available for {date}")
            return 150
            
    except Exception as e:
        logger.debug(f"Error fetching AQI data: {e}")
        return 150


def fetch_weather_data(lat, lon):
    """Fetch weather data from OpenWeather API."""
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(OPENWEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        main_data = data.get("main", {})
        temp = main_data.get("temp", 28.0)
        humidity = main_data.get("humidity", 70)
        
        logger.debug(f"✓ Weather data fetched: Temp={temp}°C, Humidity={humidity}%")
        return temp, humidity
        
    except Exception as e:
        logger.debug(f"Error fetching weather data: {e}")
        return 28.0, 70


def generate_comprehensive_enriched_dataset(base_df, analysis_df=None):
    """
    Generate comprehensive enriched dataset combining multiple sources.
    
    Args:
        base_df (pd.DataFrame): Base hospital dataset
        analysis_df (pd.DataFrame): Analysis dataset (optional)
        
    Returns:
        pd.DataFrame: Enriched comprehensive dataset
    """
    logger.info("Generating comprehensive enriched dataset...")
    
    # Convert dates and sort
    base_df["admission_date"] = pd.to_datetime(base_df["admission_date"])
    base_df.sort_values("admission_date", inplace=True)
    
    # If analysis data available, extract statistics
    analysis_stats = None
    if analysis_df is not None:
        analysis_stats = extract_admission_patterns(analysis_df)
    
    # Create date range for enrichment
    unique_dates = base_df["admission_date"].dt.date.unique()
    enriched_data = []
    
    for date in sorted(unique_dates):
        date_str = str(date)
        
        # Get records for this date
        day_records = base_df[base_df["admission_date"].dt.date == date]
        
        # Patient count
        patient_count = len(day_records)
        
        # Dominant disease type
        disease_type = day_records["disease_type"].mode()
        disease_type = disease_type[0] if len(disease_type) > 0 else "Other"
        
        # Fetch environmental data
        aqi = fetch_aqi_data(HOSPITAL_LAT, HOSPITAL_LON, date_str)
        temp, humidity = fetch_weather_data(HOSPITAL_LAT, HOSPITAL_LON)
        
        # Create enriched record
        enriched_record = {
            "admission_date": date_str,
            "patient_count": patient_count,
            "disease_type": disease_type,
            "temperature": temp,
            "humidity": humidity,
            "aqi": aqi,
            "hospital_area": day_records["hospital_area"].mode()[0] if len(day_records["hospital_area"].mode()) > 0 else "General Ward",
            "source": "enriched_from_multiple_datasets"
        }
        
        enriched_data.append(enriched_record)
        logger.info(f"Processed {date_str}: {patient_count} patients, Disease: {disease_type}")
    
    enriched_df = pd.DataFrame(enriched_data)
    
    return enriched_df, analysis_stats


def integrate_datasets():
    """
    Main function to integrate and enrich multiple hospital datasets.
    """
    try:
        logger.info("=" * 70)
        logger.info("ArogyaPredict - Enhanced Data Integration")
        logger.info("=" * 70)
        
        # Load base dataset
        logger.info("\n[STEP 1] Loading Base Hospital Dataset...")
        base_df = pd.read_csv(HOSPITAL_BASE_DATASET)
        logger.info(f"✓ Loaded {len(base_df)} records from base dataset")
        
        # Load analysis dataset
        logger.info("\n[STEP 2] Loading Hospital Analysis Dataset...")
        analysis_df = load_hospital_analysis_dataset()
        
        # Generate enriched dataset
        logger.info("\n[STEP 3] Generating Enriched Dataset...")
        enriched_df, stats = generate_comprehensive_enriched_dataset(base_df, analysis_df)
        
        # Save enriched dataset
        enriched_df.to_csv(FINAL_DATASET, index=False)
        logger.info(f"\n✓ Enriched dataset saved to {FINAL_DATASET}")
        logger.info(f"  Records: {len(enriched_df)}")
        logger.info(f"  Columns: {list(enriched_df.columns)}")
        
        # Display preview
        logger.info(f"\nDataset Preview:")
        logger.info(f"\n{enriched_df.head(10).to_string()}")
        
        # Display statistics if available
        if stats:
            logger.info(f"\n" + "=" * 70)
            logger.info("HOSPITAL ANALYSIS INSIGHTS")
            logger.info("=" * 70)
            logger.info(f"Top Conditions by Admission:")
            for condition, count in sorted(stats['by_condition'].items(), key=lambda x: x[1], reverse=True)[:5]:
                logger.info(f"  - {condition}: {count} admissions")
        
        logger.info(f"\n" + "=" * 70)
        logger.info("✓ Data integration completed successfully!")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"Error during data integration: {e}")
        return False


if __name__ == "__main__":
    success = integrate_datasets()
    if not success:
        sys.exit(1)
