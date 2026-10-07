import requests
import json

url = "https://data.go.th/api/3/action/package_show?id=rtddi"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        dataset = data["result"]
        print(f"Dataset Title: {dataset.get('title')}")
        print(f"Organization: {dataset.get('organization', {}).get('title')}")
        for resource in dataset.get("resources", []):
            print(f"Resource Name: {resource.get('name')}")
            print(f"Format: {resource.get('format')}")
            print(f"URL: {resource.get('url')}")
            print("-" * 40)
    else:
        print("Failed to get dataset info:", data)
else:
    print(f"HTTP Error: {response.status_code}")
