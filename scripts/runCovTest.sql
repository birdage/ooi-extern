CREATE OR REPLACE FUNCTION runCovTest() returns text as $$
	drop foreign table if exists covtest cascade;
	
	create foreign table covtest (
       dataset_id character varying,
       time timestamp,
       cond real,
       temp real,
       lat real,
       lon real    
) server cov_srv options (k '1',
cov_path '',
time_field 'time');

	select test3();

$$ LANGUAGE SQL ;