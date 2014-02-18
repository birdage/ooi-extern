CREATE OR REPLACE FUNCTION covTest() returns text as $$
	
	drop foreign table "d05de04c33a642cab207884675c3866f" cascade;

	create foreign table "d05de04c33a642cab207884675c3866f" ("preferred_timestamp" timestamp,"temp_L1" real,"conductivity_L1" real,"temp" real,"density" real,"port_timestamp" timestamp,"density_lookup" real,"lon" real,"lat_lookup" real,"salinity" real,"pressure" real,"lon_lookup" real,"internal_timestamp" timestamp,"time" timestamp,"lat" real,"driver_timestamp" timestamp,"pressure_L1" real,"conductivity" real,latitude real,longitude real ) server cov_srv options(k '1',cov_path '/tmp/ion/ion_test_fac5a8/cache/datasets/b90c86ef15f0415c825424d6a4706128');

	CREATE or replace VIEW "d05de04c33a642cab207884675c3866f_view" as SELECT ST_SetSRID(ST_MakePoint(10, 10),4326) as 
	geom, * from "d05de04c33a642cab207884675c3866f";


	select test3();

$$ LANGUAGE SQL ;

