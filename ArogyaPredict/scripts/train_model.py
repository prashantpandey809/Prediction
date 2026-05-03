"""
Model Training Module - ArogyaPredict
Trains a RandomForestRegressor model for patient inflow prediction.

This module:
1. Loads preprocessed data
2. Splits data into train and test sets
3. Trains RandomForestRegressor
4. Evaluates model performance (MAE, RMSE, R² Score)
5. Saves trained model as model.pkl
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    FINAL_DATASET,
    MODEL_PATH,
    ENCODER_PATH,
    TEST_SIZE,
    RANDOM_STATE,
    N_ESTIMATORS,
    MAX_DEPTH,
    MIN_SAMPLES_SPLIT,
    MIN_SAMPLES_LEAF,
)
from scripts.preprocess import DataPreprocessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Handles model training, evaluation, and persistence.
    """
    
    def __init__(self):
        """Initialize the model trainer."""
        self.model = None
        self.preprocessor = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.metrics = {}
    
    def load_and_preprocess_data(self, file_path):
        """
        Load and preprocess data.
        
        Args:
            file_path (str): Path to final dataset
            
        Returns:
            tuple: (X, y, preprocessor)
        """
        logger.info("Loading and preprocessing data...")
        preprocessor = DataPreprocessor()
        X, y, preprocessor = preprocessor.preprocess(file_path)
        
        if X is None or y is None:
            logger.error("Failed to preprocess data")
            return None, None, None
        
        self.preprocessor = preprocessor
        return X, y, preprocessor
    
    def split_data(self, X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
        """
        Split data into training and testing sets.
        
        Args:
            X (pd.DataFrame): Features
            y (pd.Series): Target variable
            test_size (float): Proportion of test set
            random_state (int): Random state for reproducibility
        """
        logger.info(f"Splitting data (test_size={test_size}, random_state={random_state})...")
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state
        )
        
        logger.info(f"✓ Training set: {len(self.X_train)} samples")
        logger.info(f"✓ Testing set: {len(self.X_test)} samples")
        logger.info(f"✓ Train/Test ratio: {len(self.X_train)/len(self.X_test):.2f}:1")
    
    def build_model(self, n_estimators=N_ESTIMATORS, max_depth=MAX_DEPTH,
                    min_samples_split=MIN_SAMPLES_SPLIT, min_samples_leaf=MIN_SAMPLES_LEAF):
        """
        Build RandomForestRegressor model.
        
        Args:
            n_estimators (int): Number of trees
            max_depth (int): Maximum tree depth
            min_samples_split (int): Minimum samples to split node
            min_samples_leaf (int): Minimum samples in leaf node
        """
        logger.info("Building RandomForestRegressor model...")
        logger.info(f"  - n_estimators: {n_estimators}")
        logger.info(f"  - max_depth: {max_depth}")
        logger.info(f"  - min_samples_split: {min_samples_split}")
        logger.info(f"  - min_samples_leaf: {min_samples_leaf}")
        
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=RANDOM_STATE,
            n_jobs=-1,  # Use all available processors
            verbose=0
        )
        
        logger.info("✓ Model built successfully")
    
    def train_model(self):
        """Train the model on training data."""
        logger.info("Training model on training set...")
        
        if self.model is None:
            logger.error("Model not built. Call build_model() first.")
            return False
        
        if self.X_train is None or self.y_train is None:
            logger.error("Training data not available. Call split_data() first.")
            return False
        
        try:
            self.model.fit(self.X_train, self.y_train)
            logger.info("✓ Model training completed")
            return True
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            return False
    
    def evaluate_model(self):
        """
        Evaluate model on test set and compute metrics.
        
        Returns:
            dict: Dictionary of evaluation metrics
        """
        logger.info("Evaluating model on test set...")
        
        if self.model is None:
            logger.error("Model not trained. Call train_model() first.")
            return None
        
        # Predictions on train and test sets
        y_train_pred = self.model.predict(self.X_train)
        y_test_pred = self.model.predict(self.X_test)
        
        # Calculate metrics
        train_mae = mean_absolute_error(self.y_train, y_train_pred)
        test_mae = mean_absolute_error(self.y_test, y_test_pred)
        
        train_rmse = np.sqrt(mean_squared_error(self.y_train, y_train_pred))
        test_rmse = np.sqrt(mean_squared_error(self.y_test, y_test_pred))
        
        train_r2 = r2_score(self.y_train, y_train_pred)
        test_r2 = r2_score(self.y_test, y_test_pred)
        
        self.metrics = {
            "train_mae": train_mae,
            "test_mae": test_mae,
            "train_rmse": train_rmse,
            "test_rmse": test_rmse,
            "train_r2": train_r2,
            "test_r2": test_r2,
        }
        
        return self.metrics
    
    def print_metrics(self):
        """Print evaluation metrics in a formatted manner."""
        if not self.metrics:
            logger.warning("No metrics available. Run evaluate_model() first.")
            return
        
        logger.info("\n" + "=" * 60)
        logger.info("MODEL EVALUATION METRICS")
        logger.info("=" * 60)
        logger.info(f"\nMean Absolute Error (MAE):")
        logger.info(f"  Training:  {self.metrics['train_mae']:.4f} patients")
        logger.info(f"  Testing:   {self.metrics['test_mae']:.4f} patients")
        
        logger.info(f"\nRoot Mean Squared Error (RMSE):")
        logger.info(f"  Training:  {self.metrics['train_rmse']:.4f} patients")
        logger.info(f"  Testing:   {self.metrics['test_rmse']:.4f} patients")
        
        logger.info(f"\nR² Score:")
        logger.info(f"  Training:  {self.metrics['train_r2']:.4f}")
        logger.info(f"  Testing:   {self.metrics['test_r2']:.4f}")
        logger.info("=" * 60)
    
    def get_feature_importance(self, top_n=10):
        """
        Get feature importance from trained model.
        
        Args:
            top_n (int): Number of top features to display
            
        Returns:
            pd.DataFrame: Feature importance dataframe
        """
        if self.model is None:
            logger.error("Model not trained. Call train_model() first.")
            return None
        
        feature_importance = pd.DataFrame({
            "feature": self.X_train.columns,
            "importance": self.model.feature_importances_
        }).sort_values("importance", ascending=False)
        
        logger.info(f"\nTop {top_n} Important Features:")
        for idx, row in feature_importance.head(top_n).iterrows():
            logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        
        return feature_importance
    
    def save_model(self, path=None):
        """
        Save trained model to file.
        
        Args:
            path (str): Path to save model (optional)
        """
        if path is None:
            path = MODEL_PATH
        
        if self.model is None:
            logger.error("Model not trained. Call train_model() first.")
            return False
        
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                pickle.dump(self.model, f)
            logger.info(f"✓ Model saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, path=None):
        """
        Load trained model from file.
        
        Args:
            path (str): Path to model file (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if path is None:
            path = MODEL_PATH
        
        try:
            with open(path, "rb") as f:
                self.model = pickle.load(f)
            logger.info(f"✓ Model loaded from {path}")
            return True
        except FileNotFoundError:
            logger.error(f"Model file not found: {path}")
            return False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def complete_training_pipeline(self, data_file):
        """
        Execute complete training pipeline.
        
        Args:
            data_file (str): Path to preprocessed data file
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Starting complete model training pipeline...")
        
        # Load and preprocess data
        X, y, _ = self.load_and_preprocess_data(data_file)
        if X is None or y is None:
            return False
        
        # Split data
        self.split_data(X, y)
        
        # Build model
        self.build_model()
        
        # Train model
        if not self.train_model():
            return False
        
        # Evaluate model
        self.evaluate_model()
        self.print_metrics()
        
        # Feature importance
        self.get_feature_importance()
        
        # Save model
        if not self.save_model():
            return False
        
        logger.info("✓ Training pipeline completed successfully!")
        return True


def main():
    """Main function to execute model training."""
    logger.info("=" * 60)
    logger.info("ArogyaPredict - Model Training Module")
    logger.info("=" * 60)
    
    trainer = ModelTrainer()
    success = trainer.complete_training_pipeline(FINAL_DATASET)
    
    if success:
        logger.info("\n✓ Model training completed successfully!")
        return trainer
    else:
        logger.error("\n✗ Model training failed!")
        sys.exit(1)


if __name__ == "__main__":
    trainer = main()
