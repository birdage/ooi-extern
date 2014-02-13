CREATE or replace VIEW covproj as 
SELECT ST_SetSRID(ST_MakePoint(lon, lat),4326) as proj, dataset_id, time, cond, temp from covtest;



CREATE OR REPLACE FUNCTION covTest() returns text as $$
	
	select test3();

	CREATE or replace VIEW covproj as SELECT ST_SetSRID(ST_MakePoint(10, 10),4326) as proj, pressure, temperature from "04f348461060421faafda860df470f95";

 	select test3();

$$ LANGUAGE SQL ;