--query che calcola la distanza tra due punti con map matching
SELECT st_distance(m1.geom::geography, m2.geom::geography)
FROM tragitto_filtered as p1, tragitto_filtered as p2, matched_point as m1, matched_point as m2
WHERE p1.id = %s AND p2.id = %s 
AND
p1.track_seg_point_id = m1.track_seg_point_id AND p2.track_seg_point_id = m2.track_seg_point_id