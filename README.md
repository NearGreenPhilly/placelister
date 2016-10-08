To run this, do the following steps:

$ virtualenv listenv

(On Linux / Mac)
$ source listenv/bin/activate
or
(On Windows)
$ listenv\scripts\activate

$ pip install -r requirements.txt

# Create the database

$ psql

$ CREATE USER kevin PASSWORD 'geodjango';
$ CREATE DATABASE placelist OWNER kevin;
$ CREATE EXTENSION postgis;