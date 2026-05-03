"""
Quick test to check data and preprocessing
"""
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import FINAL_DATASET

print("=" * 60)
print("CHECKING FINAL DATASET")
print("=" * 60)

df = pd.read_csv(FINAL_DATASET)

print(f"\nShape: {df.shape}")
print(f"\nColumns:")
for col in df.columns:
    print(f"  - {col}")

print(f"\nFirst few rows:")
print(df.head())

print(f"\nData types:")
print(df.dtypes)

print(f"\nMissing values:")
print(df.isnull().sum())

print(f"\nBasic statistics:")
print(df.describe())

print(f"\nUnique disease types: {df['disease_type'].nunique()}")
print(f"  {df['disease_type'].unique()}")

print(f"\nUnique weather conditions: {df['weather_condition'].nunique()}")
print(f"  {df['weather_condition'].unique()}")

print(f"\nHolidays in dataset: {df['is_holiday'].sum()}")

print("\n✓ Dataset check complete!")
