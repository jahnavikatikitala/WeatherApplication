#https://www.tomorrow.io/blog/creating-daily-forecasts-with-a-python-weather-api/
import requests
import json
import time

API_KEY = "<Please add your own API Key>"

#Method to download data from tomorrow API and parse it
def pull_weather_data(locations):
   url = "https://api.tomorrow.io/v4/timelines"
   response_location_map = {}
   for location in locations:
     # This is to sparse the call rate to avoid throttling. In production we would add exponential back off
     time.sleep(5)
     print('pulling weather data from tomorrow.io for location:'+location)
     querystring = {
       "location":location,
       "fields":["temperature", "cloudCover", "windSpeed"],
       "units":"imperial",
       "timesteps":"1h",
       "apikey":API_KEY}
     response = requests.request("GET", url, params=querystring)
     if(response.status_code != 200):
        raise Exception("Cannot fetch results from tomorrow.io : "+json.dumps(response.json()))
     response_location_map[location] = response
   return response_location_map
