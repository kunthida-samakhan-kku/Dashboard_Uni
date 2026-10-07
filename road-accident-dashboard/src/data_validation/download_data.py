import urllib.request
import os

url = "https://data.go.th/dataset/f5804870-7dc2-42df-86f3-769d6cc2ae23/resource/045f0036-6756-4c53-8ea6-d201b6ba6650/download/_2567.csv"
output_path = "road-accident-dashboard/data/raw/rtddi_2567.csv"

try:
    urllib.request.urlretrieve(url, output_path)
    print(f"Downloaded successfully to {output_path}")
except Exception as e:
    print(f"Error downloading: {e}")
