FROM postgres:latest
ENV POSTGRES_PASSWORD=postgrespassword
ENV POSTGRES_USER=username
ENV POSTGRES_DB=database
COPY create_weather_table.sql /docker-entrypoint-initdb.d/create_weather_table.sql

