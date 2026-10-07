import pandas as pd
import json

df = pd.read_csv("road-accident-dashboard/data/cleaned/rtddi_2567_clean.csv")

# Fill NaNs
df['age'] = df['age'].fillna(-1)
df['sex'] = df['sex'].fillna('ไม่ระบุ')
df['acc_district_name'] = df['acc_district_name'].fillna('ไม่ระบุ')
df['จ.ที่เสียชีวิต'] = df['จ.ที่เสียชีวิต'].fillna('ไม่ระบุ')
df['vehicle_merge_final'] = df['vehicle_merge_final'].fillna('ไม่ระบุพาหนะ')

# Convert date and extract month
df['dead_date_final'] = pd.to_datetime(df['dead_date_final'], errors='coerce')
df['month'] = df['dead_date_final'].dt.month.fillna(-1).astype(int)

# Bin age
def get_age_group(age):
    if age < 0: return 'ไม่ระบุ'
    if age <= 14: return '0-14'
    if age <= 24: return '15-24'
    if age <= 44: return '25-44'
    if age <= 64: return '45-64'
    return '65+'

df['age_group'] = df['age'].apply(get_age_group)

# Keep only necessary columns for the dashboard to keep it lightweight
df_dash = df[['month', 'age_group', 'sex', 'จ.ที่เสียชีวิต', 'acc_district_name', 'vehicle_merge_final']]
df_dash.columns = ['month', 'age_group', 'sex', 'province', 'district', 'vehicle']

data = df_dash.to_dict(orient='records')

with open("road-accident-dashboard/outputs/dashboard_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

print("Data exported to JSON.")
