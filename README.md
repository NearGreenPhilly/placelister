To run this, do the following steps:

# Install dependencies

- Python 2.7 or greater
- virtualenv
- PostGRES
- PostGIS
- Heroku CLI


# Create and activate virtualenv

$ virtualenv listenv

(On Linux / Mac)

$ source listenv/bin/activate

(On Windows)

$ listenv\scripts\activate


# Install necessary Python packages

$ pip install -r requirements.txt


# Create the database

$ psql

$ CREATE USER kevin PASSWORD 'geodjango';

$ CREATE DATABASE placelist OWNER kevin;

$ CREATE EXTENSION postgis;



# Run locally

$ heroku local web