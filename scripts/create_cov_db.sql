create foreign table covtest (
       dataset_id character varying,
       time character varying,
       cond real,
       temp real,
       lat character varying,
       lon character varying,
	"geom" geometry(Point,4326)		
) server cov_srv options (k '1');