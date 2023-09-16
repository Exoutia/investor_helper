import requests
import json

url = "https://api.mfapi.in/mf"

response = requests.get(url)
data = response.json()
json.dump(data, open("mutualfunds.json", "w"), indent=4)
print("Done")
