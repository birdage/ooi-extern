CREATE or replace VIEW covproj as 
SELECT ST_SetSRID(ST_MakePoint(lon, lat),4326) as proj, dataset_id, time, cond, temp from covtest;