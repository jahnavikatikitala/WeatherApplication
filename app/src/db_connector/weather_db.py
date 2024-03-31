import psycopg2
from datetime import datetime,date,timedelta
import json

MAX_NUMBER_OF_DAYS_IN_HISTORY = 3
MAX_NUMBER_OF_DAYS_IN_FUTURE = 9

# connect to postgres db
def get_connection():
   connection = psycopg2.connect(database="database", user="username", password="postgrespassword", host="db", port=5432)
   return connection

# insert into postgres db
def insert_data_weather(results,location):
   print('inserting data for weather for location:'+location)
   json_res=results.json()
   # creating and cleaning up partitions here for now, but ideally we would want to have to this done as part of different job.
   clean_partitions()
   create_new_partition()
   if json_res:
        for result in json_res.get('data',{}).get('timelines',[])[0].get('intervals',[]):
            datetime_object = datetime.strptime(result['startTime'], '%Y-%m-%dT%H:%M:%SZ')
            datetime_string = datetime_object.strftime("%Y-%m-%d %H:%M:%SZ")
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("insert into weather.weather_hourly_forecast values('"+location+"',timestamp '"+datetime_string+"','"+json.dumps(result['values'])+"'::json"+",now()) ON CONFLICT(location,weather_date) DO UPDATE SET attributes='"+json.dumps(result['values'])+"'::json,update_date=now()")
                connection.commit()
            except psycopg2.IntegrityError as e:
                connection.rollback()
                print(e)
                raise
            finally:
                connection.close()

# drop older partition
def clean_partitions():
   print('cleaning up the older partitions')
   connection = get_connection()
   cursor = connection.cursor()
   try:
       # This value can be pushed to a configuration
       date_to_drop=(date.today()-timedelta(days = MAX_NUMBER_OF_DAYS_IN_HISTORY)).strftime('%Y%m%d')
       cursor.execute("drop table if exists weather.weather_hourly_forecast_"+date_to_drop)
       connection.commit()
   except psycopg2.IntegrityError as e:
       connection.rollback()
       print(e)
       raise
   finally:
       connection.close()

# create new partitions
def create_new_partition():
   print('creating new partitions if not exists')
   connection = get_connection()
   cursor = connection.cursor()
   try:
      for ndays in range(MAX_NUMBER_OF_DAYS_IN_FUTURE):
          date_to_create=(date.today()+timedelta(days = ndays)).strftime('%Y%m%d')
          date_start = (date.today()+timedelta(days = ndays)).strftime('%Y-%m-%d') 
          date_end = (date.today()+timedelta(days = ndays+1)).strftime('%Y-%m-%d')
          cursor.execute("create table if not exists weather.weather_hourly_forecast_"+date_to_create+" PARTITION OF weather.weather_hourly_forecast FOR VALUES FROM ('"+ date_start +"') TO ('"+ date_end +"')")
      connection.commit()
   except psycopg2.IntegrityError as e:
      connection.rollback()
      print(e)
      raise
   finally:
      connection.close()

# get input locations 
def get_locations():
   connection = get_connection()
   cursor = connection.cursor()
   cursor.execute("select locations from weather.locations_data")
   records = []
   for row in cursor.fetchall(): 
     records.append(row[0])
   connection.close()
   return records 
