create foreign table csvtest (
       time timestamp,
       temp real,
       pressure real,
       conductivity real,
       density real,
       salinty real
) server csv_srv options (
       filename '/home/postgres/code/test.csv',
       skip_header '0',
       delimiter ',');

select * from csvtest;




CREATE or replace VIEW "csvtestview" as SELECT ST_SetSRID(ST_MakePoint(10, 10),4326) 
as geom, * from "csvtest";