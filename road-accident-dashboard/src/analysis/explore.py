import pandas as pd

df = pd.read_csv("road-accident-dashboard/data/cleaned/rtddi_2567_clean.csv")

print("Vehicle Types:")
print(df['vehicle_merge_final'].value_counts())

print("\nSex:")
print(df['sex'].value_counts())

print("\nTop 10 Provinces:")
print(df['จ.ที่เสียชีวิต'].value_counts().head(10))

