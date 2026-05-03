"""
Data Preprocessing Module - ArogyaPredict
Handles data cleaning, transformation, and encoding.

This module:
1. Reads final_dataset.csv
2. Handles missing values properly
3. Converts date columns to datetime
4. Encodes categorical columns (disease_type, hospital_area)
5. Prepares features and target for model training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import logging
import pickle
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    FINAL_DATASET,
    ENCODER_PATH,
    DATA_DIR,
    MODELS_DIR,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Handles all data preprocessing tasks for ArogyaPredict.
    """
    
    def __init__(self):
        """Initialize the preprocessor with empty encoders."""
        self.encoders = {}
        self.df = None
        
    def load_data(self, file_path):
        """
        Load data from CSV file.
        
        Args:
            file_path (str): Path to CSV file
            
        Returns:
            pd.DataFrame: Loaded dataset
        """
        try:
            logger.info(f"Loading data from {file_path}...")
            self.df = pd.read_csv(file_path)
            logger.info(f"✓ Loaded {len(self.df)} records")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def handle_missing_values(self):
        """
        Handle missing values in the dataset.
        Strategy: forward fill for time-series data, drop rows with critical missing values.
        """
        logger.info("Handling missing values...")
        initial_rows = len(self.df)
        
        # Check for missing values
        missing_info = self.df.isnull().sum()
        if missing_info.sum() > 0:
            logger.warning(f"Missing values found:\n{missing_info[missing_info > 0]}")
        
        # Convert admission_date to datetime for proper ordering
        if "admission_date" in self.df.columns:
            self.df["admission_date"] = pd.to_datetime(self.df["admission_date"])
            self.df.sort_values("admission_date", inplace=True)
        
        # Forward fill for numerical columns (for time-series data)
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numerical_cols] = self.df[numerical_cols].ffill().bfill()
        
        # Fill missing categorical values with "Unknown" or "None"
        categorical_cols = self.df.select_dtypes(include=["object"]).columns
        for col in categorical_cols:
            self.df[col] = self.df[col].fillna("None")
        
        final_rows = len(self.df)
        rows_removed = initial_rows - final_rows
        
        if rows_removed > 0:
            logger.warning(f"✓ Removed {rows_removed} rows with missing values")
        else:
            logger.info("✓ No missing values found")
        
        return self.df
    
    def encode_categorical_columns(self, fit=True):
        """
        Encode categorical columns using LabelEncoder.
        
        Args:
            fit (bool): Whether to fit new encoders or use existing ones
            
        Returns:
            pd.DataFrame: Dataset with encoded categorical columns
        """
        logger.info("Encoding categorical columns...")
        
        categorical_cols = ["disease_type", "hospital_area", "weather_condition", "holiday_name"]
        
        for col in categorical_cols:
            if col not in self.df.columns:
                logger.warning(f"Column '{col}' not found in dataset, skipping...")
                continue
            
            if fit:
                # Create new encoder
                encoder = LabelEncoder()
                self.df[f"{col}_encoded"] = encoder.fit_transform(self.df[col])
                self.encoders[col] = encoder
                logger.info(f"✓ Encoded '{col}' with {len(encoder.classes_)} classes: {list(encoder.classes_)}")
            else:
                # Use existing encoder
                if col in self.encoders:
                    self.df[f"{col}_encoded"] = self.encoders[col].transform(self.df[col])
                    logger.info(f"✓ Applied existing encoder for '{col}'")
                else:
                    logger.warning(f"No encoder found for '{col}', fitting new one...")
                    encoder = LabelEncoder()
                    self.df[f"{col}_encoded"] = encoder.fit_transform(self.df[col])
                    self.encoders[col] = encoder
        
        return self.df
    
    def create_features_and_target(self):
        """
        Create feature matrix and target variable for model training.
        
        Returns:
            tuple: (X, y) where X is features and y is target
        """
        logger.info("Creating features and target variable...")
        
        # Drop non-feature columns and original categorical columns (but only if they exist)
        cols_to_drop = [
            "admission_date", "disease_type", "hospital_area", 
            "weather_condition", "holiday_name", "source"
        ]
        # Only drop columns that actually exist in the dataframe
        cols_to_drop = [col for col in cols_to_drop if col in self.df.columns]
        
        # Get all feature columns (exclude the ones we're dropping)
        feature_cols = [col for col in self.df.columns if col not in cols_to_drop]
        
        # Target variable - try multiple possible names
        target_col = None
        if "patient_count" in self.df.columns:
            target_col = "patient_count"
        elif "actual_patient_count" in self.df.columns:
            target_col = "actual_patient_count"
        
        if target_col and target_col in feature_cols:
            X = self.df[feature_cols].drop(target_col, axis=1)
            y = self.df[target_col]
            logger.info(f"✓ Target variable: '{target_col}'")
            logger.info(f"✓ Features ({len(X.columns)}): {list(X.columns)}")
            logger.info(f"✓ Target shape: {y.shape}")
        else:
            logger.error(f"Target column '{target_col}' not found in features")
            return None, None
        
        logger.info(f"✓ Dataset shape: {X.shape}")
        
        return X, y
    
    def validate_data(self):
        """
        Validate the preprocessed data.
        
        Returns:
            bool: True if validation passes, False otherwise
        """
        logger.info("Validating preprocessed data...")
        
        checks = {
            "No missing values": self.df.isnull().sum().sum() == 0,
            "Correct shape": len(self.df) > 0,
            "Numeric features present": len(self.df.select_dtypes(include=[np.number]).columns) > 0,
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            logger.info(f"{status} {check_name}")
            all_passed = all_passed and passed
        
        return all_passed
    
    def save_encoders(self, path=None):
        """
        Save encoders to file for later use in predictions.
        
        Args:
            path (str): Path to save encoders (optional)
        """
        if path is None:
            path = ENCODER_PATH
        
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                pickle.dump(self.encoders, f)
            logger.info(f"✓ Encoders saved to {path}")
        except Exception as e:
            logger.error(f"Error saving encoders: {e}")
    
    def preprocess(self, file_path):
        """
        Complete preprocessing pipeline.
        
        Args:
            file_path (str): Path to dataset CSV file
            
        Returns:
            tuple: (X, y, preprocessor) - Features, target, and preprocessor object
        """
        logger.info("Starting complete preprocessing pipeline...")
        
        # Load data
        if self.load_data(file_path) is None:
            return None, None, None
        
        # Handle missing values
        self.handle_missing_values()
        
        # Encode categorical columns
        self.encode_categorical_columns(fit=True)
        
        # Validate data
        if not self.validate_data():
            logger.warning("Data validation had some issues, but continuing...")
        
        # Create features and target
        X, y = self.create_features_and_target()
        
        # Save encoders
        self.save_encoders()
        
        logger.info("✓ Preprocessing pipeline completed!")
        
        return X, y, self


def main():
    """Main function to execute preprocessing pipeline."""
    logger.info("=" * 60)
    logger.info("ArogyaPredict - Data Preprocessing Module")
    logger.info("=" * 60)
    
    preprocessor = DataPreprocessor()
    X, y, _ = preprocessor.preprocess(FINAL_DATASET)
    
    if X is not None and y is not None:
        logger.info("\n" + "=" * 60)
        logger.info("PREPROCESSING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Features shape: {X.shape}")
        logger.info(f"Target shape: {y.shape}")
        logger.info(f"\nFeature names: {list(X.columns)}")
        logger.info(f"\nTarget statistics:\n{y.describe()}")
        logger.info("\n✓ Data is ready for model training!")
        return X, y
    else:
        logger.error("\n✗ Preprocessing failed!")
        sys.exit(1)


if __name__ == "__main__":
    X, y = main()
