# Road Accidents in Thailand: Where, When, Who, and Why?

This project is a REAL-DATA-ONLY interactive dashboard built to analyze road accident fatalities in Thailand. 
It uses ONLY verified open data from the Thai government. 
**No synthetic, mock, or AI-generated data is used in this dashboard.**

## Project Structure

```
road-accident-dashboard/
├── README.md
├── HANDOFF.md
├── data/
│   ├── raw/                 # Original downloaded datasets (e.g., rtddi_2567.csv)
│   └── cleaned/             # Cleaned versions of the datasets
├── src/
│   ├── data_validation/     # Scripts to check and download from data.go.th
│   ├── data_cleaning/       # Scripts to clean the data
│   ├── analysis/            # Scripts for data exploration and JSON generation
│   └── visualization/       # Scripts to build the interactive HTML dashboard
├── outputs/
│   └── road_accident_dashboard.html # The final interactive dashboard
└── sources/
    └── data_sources.csv     # Traceability log for data sources
```

## How to use

Simply open `outputs/road_accident_dashboard.html` in any modern web browser to view the interactive dashboard.

## Methodology

1. Data was sourced from `data.go.th`, specifically the "rtddi" dataset (ระบบบูรณาการข้อมูลการตายจากอุบัติเหตุทางถนน 3 ฐาน ปี 2567).
2. The CSV dataset was validated and downloaded without modification to the `data/raw/` folder.
3. Missing values for critical fields were flagged.
4. An interactive single-page dashboard was generated using Vue.js and Chart.js, injecting only verified records.

## Data Constraints

Fields such as detailed accident causes (e.g., speeding) and exact time of day were missing from this specific mortality dataset. Per the strict project policy, these gaps are documented in the dashboard rather than filled with fabricated numbers.
