CREATE SCHEMA weather;
CREATE TABLE weather.weather_hourly_forecast( 
  location varchar(20), 
  weather_date  TIMESTAMP without time zone, 
  attributes  jsonb, 
  update_date date,
  PRIMARY KEY (location,weather_date)
) 
PARTITION BY RANGE (weather_date);

create table  weather.locations_data (
 locations varchar(30) PRIMARY KEY
);

insert into weather.locations_data values('25.8600,-97.4200');
insert into weather.locations_data values('25.9000,-97.5200');
insert into weather.locations_data values('25.9000,-97.4800');
insert into weather.locations_data values('25.9000,-97.4400');
insert into weather.locations_data values('25.9000,-97.4000');
insert into weather.locations_data values('25.9200,-97.3800');
insert into weather.locations_data values('25.9400,-97.5400');
insert into weather.locations_data values('25.9400,-97.5200');
insert into weather.locations_data values('25.9400,-97.4800');
insert into weather.locations_data values('25.9400,-97.4400');
