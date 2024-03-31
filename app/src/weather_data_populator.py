import requests
import response
import psycopg2
from datetime import datetime
import json
from tomorrow_api.weather_api import pull_weather_data 
from db_connector.weather_db import insert_data_weather, get_locations
import time


# This is the start function of collection of weather data and populating it to the database tables
# Ideally we should catch any exceptions here and handle it appropriately, some cases we may consider to alarm but not stop the job from running.
def execute():
    while True:    
       response_location_map=pull_weather_data(get_locations())
       for location,response in response_location_map.items():
         insert_data_weather(response,location)
       # pulls data hourly
       time.sleep(60*60)
       
execute() 
