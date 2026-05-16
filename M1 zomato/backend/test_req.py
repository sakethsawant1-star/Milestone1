import requests

url = "http://localhost:5001/api/recommend"
payload = {
    "staticContext": {
        "location": "Banashankari",
        "budget": "low",
        "cuisine": "Any"
    },
    "nuanceContext": "family friendly"
}
response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
