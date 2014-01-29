CREATE OR REPLACE FUNCTION runCovTest() returns text as $$
	drop foreign table covtest;
	
	create foreign table covtest (
       dataset_id character varying,
       time character varying,
       cond real,
       temp real,
       lat character varying,
       lon character varying,
	"geom" geometry(Point,4326)		
) server cov_srv options (k '1');

	select test3();

$$ LANGUAGE SQL ;