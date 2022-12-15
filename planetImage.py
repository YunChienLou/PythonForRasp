import geocoder
from datetime import datetime
import requests

today_time_stamp = datetime.today().strftime('%Y-%m-%d')
api_key = 'wVeS2K3hadwSiaxsEwG40cFP8thSverq73JmhCEj'
myloc = geocoder.ip('me')
lat = str(round(myloc.lat, 2))
lng = str(round(myloc.lng, 2))

response_API = requests.get('https://api.nasa.gov/planetary/earth/imagery?lon=' +
                            lng + '&lat='+lat + '&date='+today_time_stamp + '&api_key='+api_key)
print(today_time_stamp)
print(response_API)

