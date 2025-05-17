import requests

OPENROUTER_API_KEY = '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'

url = "https://openrouter.ai/api/v1/models"
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}"
}

res = requests.get(url, headers=headers)
print(res.status_code)
print(res.text)
