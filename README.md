An application that scrapes weather data from Tomorrow IO API for a set of geographic locations, inserts that data to postgres and lets you query the data via Jupyter! 
Services of this application are defined as docker containers and are runnable locally.

Here are the pre-requisities before you try out the application:
Create an account to access tomorrowAPI: https://docs.tomorrow.io/reference/welcome. Once you create an account, you can get the APIKey.

Steps to run the application:
1. Checkout the git code and then run `docker-compose up --build`
2. Click the jupyter url which can be accessed via localhost:8887 [link will show up in logs of above command]
3. Connect to sql
```
%load_ext sql
%env DATABASE_URL=postgresql://username:postgrespassword@db/database
```
4. Below are the list of queries that you can try out on Jupyter to test the application: 
   a. To test the latest temperature and latest windspeed (let's say today's date is April 1st 2024, the latest temp will show you data for April 5th, 2024 and the latest hour that we could pull from tommorow.io) for all of the geo locations, you can run this query:
```
%sql
SELECT location,
       weather_date AS latest_weather_date,
       (attributes->>'temperature')::numeric AS latest_temperature,
       (attributes->>'windSpeed')::numeric as windSpeed
FROM (
    SELECT location,
           weather_date,
           attributes,
           ROW_NUMBER() OVER (PARTITION BY location ORDER BY weather_date DESC) AS rn
    FROM weather.weather_hourly_forecast
    WHERE location = '25.8600, -97.4200'
) AS subquery
WHERE rn = 1;
```

 b. To test the latest temperature and latest windspeed: (Say today is April 1st 10:25AM, it retrieves the data for April 1st 10:00AM) for all of the geo locations, you can run this query. By current :
```
%sql SELECT location, weather_date, (attributes->>'temperature')::numeric AS latest_temperature, (attributes->>'windSpeed')::numeric as windSpeed from weather.weather_hourly_forecast where weather_date = DATE_TRUNC('HOUR', timezone('utc', now()));
```

   c. To see an hourly time series of temperature from a day ago to 5 days in the future for a selected location, run this query:
```
%sql SELECT location, weather_date, (attributes->>'temperature')::numeric AS latest_temperature from weather.weather_hourly_forecast where weather_date >= timezone('utc', now()) - interval '1 day' and weather_date <= timezone('utc', now()) + interval '5 day' and location = '25.8600,-97.4200';
```

List of services:
1. Postgres
Created a new postgres instance to initialize the weather information table and the location table. The component #2(Weather Information fetcher) connects to this database and pushes the information fetched from tomorrow.io api. The weather information table is created as a partitioned table which is partitioned by date. This allows for dropping older data easily by dropping the partition table if the scale grows. Currently, the Weather Information fetcher creates the partitions as well drops the older partitions, this can be moved to a different job(scheduler) - which runs on a daily basis to create new partitions and drops older partitions.

2. Weather Information fetcher
This application will get current and forecast information from tomorrow.io timeline API for locations present in 'weather.locations' table. The information is then published to postgres  updating previous entries and inserting new entries. Note that for this application, the forecast information is updated every hour.  

3. Jupyter 
The required libraries are available in the docker container to connect to postgres.  


Rationale behind the design/technology choices:
1. Why Postgres ?
SQL query language is the best choice for analytical use-cases, hence I went with a relational database. Materialized views of Postgres might come in handy down the lane to handle complex analytical use-cases.

2. Why store geo-locations in database instead of config file?
Storing geo-locations in database instead of config file, allows for a scalable solution.

3. Why single threaded?
The best approach would be to pull the data in parallel using multithreaded approach but, for this application I chose single thread to avoid throttle issues and also because of the free plan that I subscribed to on tommorow.io.

4. Why store the attributes like windSpeed, temperature as json?
In case of scaling this application down the lane, adding new attributes would not need an "alter table" operation.


Potential improvements:
1. Database column for location can be modelled as POINT datatype instead of VARCHAR(20). The current schema has limitations, say, if a space is added in between longitude and lattitude they will be considered as different locations though they are not. This also allows to perform nearest neighbor type of queries as well with postgres. And there are indexes specifically for that.
2. If it's a production environment,the best practices to incorporate would be to alarm on failures, alarm on increase in load latencies and alarm on database related metrics(eg:CPU utilization).
3. Moving the configuration parameters to a single file to allow users to tweak required config paramters as their needs suits. Could also consider Temporal to schedule when at scale.
4. Single threaded application wont scale up well and even single host wont scale up well. More over single host can become a single point of failure. Sharding would be preferred in case of scale.
