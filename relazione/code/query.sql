SELECT strade.osm_id FROM tragitto_filtered as t, strade_open_street_map as strade 
WHERE t.track_seg_point_id = %s AND strade.highway <> 'pedestrian' AND strade.highway <> 'footway'
ORDER BY st_distance(t.geom, strade.geom) 
LIMIT 1;