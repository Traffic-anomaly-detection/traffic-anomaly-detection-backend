CREATE DATABASE tadacc;

CREATE TABLE accident(
  accident_id SERIAL PRIMARY KEY,
  road_no INT,
  km INT,
  lat FLOAT,
  lon FLOAT,
  date_time date,
  time_stamp TIMESTAMP
);