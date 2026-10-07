import pandas as pd
import os

input_file = "road-accident-dashboard/data/raw/rtddi_2567.csv"
output_file = "road-accident-dashboard/data/cleaned/rtddi_2567_clean.csv"

# Read the data
df = pd.read_csv(input_file)

# Print columns
print("Original Columns:")
print(df.columns.tolist())

# Clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
print("\nCleaned Columns:")
print(df.columns.tolist())

# Inspect the data
print(f"\nTotal rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print("\nMissing values:")
print(df.isnull().sum())

# Clean specific columns
# E.g., handling missing or fixing data types
# For Dead Date Final
if 'dead_date_final' in df.columns:
    df['dead_date_final'] = pd.to_datetime(df['dead_date_final'], errors='coerce')

# Save cleaned data
df.to_csv(output_file, index=False)
print(f"\nSaved cleaned data to {output_file}")
