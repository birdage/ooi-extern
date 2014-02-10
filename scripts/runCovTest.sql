CREATE OR REPLACE FUNCTION runCovTest() returns text as $$
	drop foreign table covtest;
	
	create foreign table covtest (
       dataset_id character varying,
       time timestamp,
       cond real,
       temp real,
       lat real,
       lon real,
       "geom" geometry(Point,4326)        
) server cov_srv options (k '1',
cov_path '/Users/rpsdev/ooi_test_data/63169092-1FCD-4681-8E15-5320098DE1E4',
time_field 'time');

	select test3();

$$ LANGUAGE SQL ;