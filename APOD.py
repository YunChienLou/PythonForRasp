import requests

api_key = 'wVeS2K3hadwSiaxsEwG40cFP8thSverq73JmhCEj'
response_API = requests.get('https://api.nasa.gov/planetary/apod?api_key='+api_key)
data = response_API.json()
print(data['url'])