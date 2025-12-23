import requests

url = 'http://localhost:8000/'

request = requests.get(url)
print(request.json())