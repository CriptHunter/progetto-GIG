SELECT st_closestpoint(strade.geom, t.geom)
FROM strade_open_street_map as strade, tragitto_filtered as t
WHERE CAST(strade.osm_id AS int) = %s AND t.track_seg_point_id = %s;