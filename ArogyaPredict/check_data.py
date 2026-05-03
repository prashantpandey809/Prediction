import pandas as pd

df = pd.read_csv("data/final_dataset.csv")
print("Disease Types in training data:")
print(df['disease_type'].unique())
print(f"\nWeather Conditions in training data:")
print(df['weather_condition'].unique())
print(f"\nHoliday Names in training data:")
print(df['holiday_name'].unique())
print(f"\nData shape: {df.shape}")
