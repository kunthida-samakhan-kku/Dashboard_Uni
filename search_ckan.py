import requests
import json

urls = [
    "https://data.go.th/api/3/action/package_search?q=มหาวิทยาลัยขอนแก่น",
    "https://data.go.th/api/3/action/package_search?q=มัธยมศึกษาตอนปลาย",
    "https://data.go.th/api/3/action/package_search?q=อุดมศึกษา"
]

for url in urls:
    print(f"Searching: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get('result', {}).get('results', [])
        print(f"Found {len(results)} results")
        for res in results[:5]:
            print(f"- {res.get('title')}")
    else:
        print(f"Error: {response.status_code}")
    print("="*40)
