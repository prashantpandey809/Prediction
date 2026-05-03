"""
Data Analysis & Insights Module - ArogyaPredict
Provides comprehensive analysis of hospital datasets and generates insights.
"""

import pandas as pd
import numpy as np
import logging
import sys
import os
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATA_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class HospitalDataAnalyzer:
    """Comprehensive analysis of hospital datasets."""
    
    def __init__(self):
        self.base_df = None
        self.analysis_df = None
        self.enriched_df = None
    
    def load_datasets(self):
        """Load all available hospital datasets."""
        logger.info("Loading hospital datasets...")
        
        # Load base dataset
        base_file = os.path.join(DATA_DIR, "hospital_base_dataset.csv")
        if os.path.exists(base_file):
            self.base_df = pd.read_csv(base_file)
            logger.info(f"✓ Base dataset: {len(self.base_df)} records")
        
        # Load analysis dataset
        analysis_file = os.path.join(DATA_DIR, "hospital_analysis_dataset.csv")
        if os.path.exists(analysis_file):
            self.analysis_df = pd.read_csv(analysis_file)
            logger.info(f"✓ Analysis dataset: {len(self.analysis_df)} records")
        
        # Load enriched dataset
        enriched_file = os.path.join(DATA_DIR, "final_dataset.csv")
        if os.path.exists(enriched_file):
            self.enriched_df = pd.read_csv(enriched_file)
            logger.info(f"✓ Enriched dataset: {len(self.enriched_df)} records")
    
    def analyze_clinical_outcomes(self):
        """Analyze clinical outcomes from analysis dataset."""
        if self.analysis_df is None:
            logger.warning("Analysis dataset not available")
            return
        
        logger.info("\n" + "=" * 70)
        logger.info("CLINICAL OUTCOMES ANALYSIS")
        logger.info("=" * 70)
        
        if "Outcome" in self.analysis_df.columns:
            outcomes = self.analysis_df["Outcome"].value_counts()
            logger.info("\nOutcome Distribution:")
            for outcome, count in outcomes.items():
                pct = (count / len(self.analysis_df)) * 100
                logger.info(f"  {outcome}: {count} patients ({pct:.1f}%)")
        
        if "Readmission" in self.analysis_df.columns:
            readmissions = self.analysis_df["Readmission"].value_counts()
            logger.info("\nReadmission Status:")
            for status, count in readmissions.items():
                pct = (count / len(self.analysis_df)) * 100
                logger.info(f"  {status}: {count} patients ({pct:.1f}%)")
        
        if "Satisfaction" in self.analysis_df.columns:
            avg_satisfaction = self.analysis_df["Satisfaction"].mean()
            logger.info(f"\nPatient Satisfaction Score: {avg_satisfaction:.2f}/5")
        
        if "Length_of_Stay" in self.analysis_df.columns:
            avg_stay = self.analysis_df["Length_of_Stay"].mean()
            logger.info(f"Average Hospital Stay: {avg_stay:.1f} days")
    
    def analyze_disease_distribution(self):
        """Analyze disease distribution across datasets."""
        logger.info("\n" + "=" * 70)
        logger.info("DISEASE DISTRIBUTION ANALYSIS")
        logger.info("=" * 70)
        
        # Base dataset
        if self.base_df is not None and "disease_type" in self.base_df.columns:
            logger.info("\nBase Dataset - Disease Types:")
            diseases = self.base_df["disease_type"].value_counts()
            for disease, count in diseases.items():
                pct = (count / len(self.base_df)) * 100
                logger.info(f"  {disease}: {count} ({pct:.1f}%)")
        
        # Analysis dataset
        if self.analysis_df is not None and "Condition" in self.analysis_df.columns:
            logger.info("\nAnalysis Dataset - Conditions:")
            conditions = self.analysis_df["Condition"].value_counts()
            for condition, count in conditions.head(10).items():
                pct = (count / len(self.analysis_df)) * 100
                logger.info(f"  {condition}: {count} ({pct:.1f}%)")
    
    def analyze_cost_patterns(self):
        """Analyze cost patterns from analysis dataset."""
        if self.analysis_df is None or "Cost" not in self.analysis_df.columns:
            logger.warning("Cost data not available")
            return
        
        logger.info("\n" + "=" * 70)
        logger.info("COST ANALYSIS")
        logger.info("=" * 70)
        
        logger.info(f"\nCost Statistics:")
        logger.info(f"  Average Cost: ₹{self.analysis_df['Cost'].mean():,.2f}")
        logger.info(f"  Median Cost: ₹{self.analysis_df['Cost'].median():,.2f}")
        logger.info(f"  Min Cost: ₹{self.analysis_df['Cost'].min():,.2f}")
        logger.info(f"  Max Cost: ₹{self.analysis_df['Cost'].max():,.2f}")
        logger.info(f"  Total Cost: ₹{self.analysis_df['Cost'].sum():,.2f}")
        
        if "Condition" in self.analysis_df.columns:
            logger.info(f"\nAverage Cost by Condition (Top 5):")
            cost_by_condition = self.analysis_df.groupby("Condition")["Cost"].mean().sort_values(ascending=False)
            for condition, cost in cost_by_condition.head(5).items():
                logger.info(f"  {condition}: ₹{cost:,.2f}")
    
    def analyze_demographics(self):
        """Analyze demographic patterns."""
        if self.analysis_df is None:
            logger.warning("Demographic data not available")
            return
        
        logger.info("\n" + "=" * 70)
        logger.info("DEMOGRAPHIC ANALYSIS")
        logger.info("=" * 70)
        
        if "Age" in self.analysis_df.columns:
            logger.info(f"\nAge Statistics:")
            logger.info(f"  Average Age: {self.analysis_df['Age'].mean():.1f} years")
            logger.info(f"  Median Age: {self.analysis_df['Age'].median():.1f} years")
            logger.info(f"  Age Range: {self.analysis_df['Age'].min()}-{self.analysis_df['Age'].max()} years")
        
        if "Gender" in self.analysis_df.columns:
            logger.info(f"\nGender Distribution:")
            gender = self.analysis_df["Gender"].value_counts()
            for g, count in gender.items():
                pct = (count / len(self.analysis_df)) * 100
                logger.info(f"  {g}: {count} ({pct:.1f}%)")
    
    def analyze_environmental_patterns(self):
        """Analyze environmental patterns in enriched dataset."""
        if self.enriched_df is None:
            logger.warning("Enriched dataset not available")
            return
        
        logger.info("\n" + "=" * 70)
        logger.info("ENVIRONMENTAL PATTERNS ANALYSIS")
        logger.info("=" * 70)
        
        if "temperature" in self.enriched_df.columns:
            logger.info(f"\nTemperature Statistics:")
            logger.info(f"  Average: {self.enriched_df['temperature'].mean():.1f}°C")
            logger.info(f"  Range: {self.enriched_df['temperature'].min():.1f}°C - {self.enriched_df['temperature'].max():.1f}°C")
        
        if "humidity" in self.enriched_df.columns:
            logger.info(f"\nHumidity Statistics:")
            logger.info(f"  Average: {self.enriched_df['humidity'].mean():.1f}%")
            logger.info(f"  Range: {self.enriched_df['humidity'].min():.1f}% - {self.enriched_df['humidity'].max():.1f}%")
        
        if "aqi" in self.enriched_df.columns:
            logger.info(f"\nAir Quality Index (AQI) Statistics:")
            logger.info(f"  Average: {self.enriched_df['aqi'].mean():.0f}")
            logger.info(f"  Range: {self.enriched_df['aqi'].min():.0f} - {self.enriched_df['aqi'].max():.0f}")
        
        if "patient_count" in self.enriched_df.columns:
            logger.info(f"\nPatient Count Statistics:")
            logger.info(f"  Average Daily: {self.enriched_df['patient_count'].mean():.1f}")
            logger.info(f"  Max Daily: {self.enriched_df['patient_count'].max():.0f}")
            logger.info(f"  Min Daily: {self.enriched_df['patient_count'].min():.0f}")
    
    def generate_insights(self):
        """Generate actionable insights from data."""
        logger.info("\n" + "=" * 70)
        logger.info("KEY INSIGHTS & RECOMMENDATIONS")
        logger.info("=" * 70)
        
        insights = []
        
        # Insight 1: High cost conditions
        if self.analysis_df is not None and "Cost" in self.analysis_df.columns:
            avg_cost = self.analysis_df["Cost"].mean()
            high_cost_cases = self.analysis_df[self.analysis_df["Cost"] > avg_cost * 2]
            if len(high_cost_cases) > 0:
                insights.append(f"High-cost treatments ({len(high_cost_cases)} cases) account for significant resource allocation")
        
        # Insight 2: Readmission patterns
        if self.analysis_df is not None and "Readmission" in self.analysis_df.columns:
            readmit_rate = (self.analysis_df["Readmission"] == "Yes").sum() / len(self.analysis_df) * 100
            if readmit_rate > 20:
                insights.append(f"Readmission rate is {readmit_rate:.1f}% - consider enhanced follow-up protocols")
        
        # Insight 3: Environmental impact
        if self.enriched_df is not None:
            if "aqi" in self.enriched_df.columns and "patient_count" in self.enriched_df.columns:
                high_aqi = self.enriched_df[self.enriched_df["aqi"] > 200]
                if len(high_aqi) > 0:
                    avg_patients_high_aqi = high_aqi["patient_count"].mean()
                    insights.append(f"High AQI levels correlate with increased patient influx (avg {avg_patients_high_aqi:.1f} patients)")
        
        # Display insights
        if insights:
            for i, insight in enumerate(insights, 1):
                logger.info(f"{i}. {insight}")
        else:
            logger.info("Analyze datasets to generate insights")
    
    def run_full_analysis(self):
        """Run complete analysis pipeline."""
        logger.info("=" * 70)
        logger.info("AROGYA PREDICT - COMPREHENSIVE DATA ANALYSIS")
        logger.info("=" * 70)
        
        self.load_datasets()
        self.analyze_clinical_outcomes()
        self.analyze_disease_distribution()
        self.analyze_cost_patterns()
        self.analyze_demographics()
        self.analyze_environmental_patterns()
        self.generate_insights()
        
        logger.info("\n" + "=" * 70)
        logger.info("✓ Analysis completed successfully!")
        logger.info("=" * 70)


def main():
    """Main execution function."""
    analyzer = HospitalDataAnalyzer()
    analyzer.run_full_analysis()


if __name__ == "__main__":
    main()
