CREATE OR REPLACE FUNCTION covTest() returns text as $$
	
	drop foreign table "ae073a051a0644c1a6094fbb302ee256" cascade;

	create foreign table "ae073a051a0644c1a6094fbb302ee256" ("preferred_timestamp" timestamp,"temp_L1" real,"conductivity_L1" real,"temp" real,"density" real,"port_timestamp" timestamp,"lon" real,"lat_lookup" real,"salinity" real,"pressure" real,"lon_lookup" real,"internal_timestamp" timestamp,"time" timestamp,"lat" real,"driver_timestamp" timestamp,"pressure_L1" real,"beam_samples" real,"conductivity" real,latitude real,longitude real ) server cov_srv options(k '1',cov_path '/tmp/ion/ion_test_ff3ae3/cache/datasets/b62e9210d1e1446082d6523c1f7bd461');

	CREATE or replace VIEW covproj as SELECT ST_SetSRID(ST_MakePoint(10, 10),4326) as 
	geom, temp from "ae073a051a0644c1a6094fbb302ee256";

 	select test3();

$$ LANGUAGE SQL ;


