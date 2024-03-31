#Deriving the latest base image
FROM python:latest
RUN pip3 install --no-cache-dir requests response psycopg2

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY src/ .
#COPY tomorrow_api/weather_api.py ./tomorrow_api/
#COPY db_connector/weather_db.py ./db_connector/
#COPY constants/constants.py ./constants/
# Now the structure looks like this '/usr/app/src/test.py'


#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./weather_data_populator.py"]

