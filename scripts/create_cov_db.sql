create foreign table covtest (
       dataset_id character varying,
       time character varying,
       cond real,
       temp real,
       lat character varying,
       lon character varying,
	"geom" geometry(Point,4326)		
) server cov_srv options (k '1',cov_path '/tmp/ion/ion_test_9615be/cache/datasets/44afbd5858c44a8494f171d15e76d0ab');