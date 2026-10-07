import pandas as pd
import os

def clean_high_school_data():
    raw_file = 'data/raw/khonkaen_high_school.csv'
    processed_file = 'data/processed/khonkaen_high_school_cleaned.csv'
    
    if not os.path.exists(raw_file):
        print("Raw data file not found.")
        return
    
    try:
        # Load with TIS-620/cp874 encoding
        df = pd.read_csv(raw_file, encoding='cp874')
        
        # Rename columns to standard english names based on observation
        # e.g., 'ปีงบประมาณ', 'จังหวัด', 'ชื่อตัวชี้วัด', 'จำนวน', 'หน่วย', 'แหล่งที่มา'
        df.columns = ['year', 'province', 'indicator', 'student_count', 'unit', 'source']
        
        # Clean student_count (remove commas, trim, and convert to int)
        df['student_count'] = df['student_count'].astype(str).str.replace(',', '').str.strip()
        df['student_count'] = pd.to_numeric(df['student_count'], errors='coerce')
        
        # Drop rows with NaN in student_count if any
        df = df.dropna(subset=['student_count'])
        df['student_count'] = df['student_count'].astype(int)
        
        # Save processed data
        os.makedirs('data/processed', exist_ok=True)
        df.to_csv(processed_file, index=False, encoding='utf-8')
        print(f"Data cleaned and saved to {processed_file}")
        
    except Exception as e:
        print(f"Error cleaning data: {e}")

if __name__ == '__main__':
    clean_high_school_data()
