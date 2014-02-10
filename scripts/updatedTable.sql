CREATE OR REPLACE FUNCTION runCovTest(dataset_id,params,geom) returns text as $$

       #param dict list param(param, 'param type')
       #geom dict list geom(geom, 'geom type') i.e point && (geom, 'geom ref') i.e 4326

       #data products i.e are two datasets could have different data 

	drop foreign table "dataset_id";
	
	create foreign table "dataset_id" (
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



$$ LANGUAGE SQL ;