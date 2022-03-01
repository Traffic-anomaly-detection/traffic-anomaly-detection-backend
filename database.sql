CREATE DATABASE tadacc;

CREATE TABLE accident(
  accident_id SERIAL PRIMARY KEY,
  road_no INT NOT NULL,
  km INT NOT NULL,
  direction VARCHAR(256),
  inflow_units INT NOT NULL,
  outflow_units INT NOT NULL,
  samecell_units INT NOT NULL,
  all_units INT NOT NULL,
  lat FLOAT NOT NULL,
  lon FLOAT NOT NULL,
  date_time date NOT NULL,
  time_stamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);