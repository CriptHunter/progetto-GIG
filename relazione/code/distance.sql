--query che calcola la distanza tra due punti
SELECT st_distance(p1.geom::geography, p2.geom::geography)
FROM tragitto_filtered as p1, tragitto_filtered as p2
WHERE p1.id = %s AND p2.id = %s