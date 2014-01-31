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
) server cov_srv options (k '1',cov_path '/tmp/ion/ion_test_9615be/cache/datasets/44afbd5858c44a8494f171d15e76d0ab');

	select test3();

$$ LANGUAGE SQL ;