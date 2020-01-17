#ritorna tutti i punti del tragitto
get_points_query = '''SELECT distinct id, time 
					  FROM tragitto_filtered
					  ORDER BY time;'''

#query che cancella tutti i punti generati dal calcolo della velocità
delete_speed_query = '''DELETE FROM speed'''

#query che cancella tutti i punti generati dal calcolo della velocità
delete_speed_mm_query = '''DELETE FROM speed_mm'''

#query che calcola la distanza tra due punti
distance_query = '''SELECT st_distance(p1.geom::geography, p2.geom::geography)
					FROM tragitto_filtered as p1, tragitto_filtered as p2
					WHERE p1.id = %s AND p2.id = %s'''

#query che calcola la distanza tra due punti con map matching
distance_map_matched_query = '''SELECT st_distance(m1.geom::geography, m2.geom::geography)
								FROM tragitto_filtered as p1, tragitto_filtered as p2, matched_point as m1, matched_point as m2
								WHERE p1.id = %s AND p2.id = %s 
								AND
							    p1.track_seg_point_id = m1.track_seg_point_id AND p2.track_seg_point_id = m2.track_seg_point_id''' 

#query che inserisce le velocità calcolate nella tabella speed
insert_speeds_query = '''INSERT INTO speed 
				   		 VALUES (%s, %s, %s, %s)''' #id idp1 idp2 speed

#query che inserisce le velocità calcolate nella tabella speed map_matched
insert_speeds_mm_query = '''INSERT INTO speed_mm
				   			VALUES (%s, %s, %s, %s)''' 


def avg_speed(connection):
	print('-'*100)
	print("AVG SPEED:")
	cursor = connection.cursor()

	#lista di tuple(id_p1, id_p2, Δt, Δs)
	speeds_list = []

	cursor.execute(delete_speed_query)
	cursor.execute(delete_speed_mm_query)
	connection.commit()

	cursor.execute(get_points_query)

	points = cursor.fetchall()

	#velocità senza map matching
	avg_speed = insert_speed(points, distance_query, insert_speeds_query, cursor, speeds_list)
	print("average speed, no map matching = {} m/s = {} km/h".format(avg_speed, avg_speed*3.6))

	speeds_list.clear()
	#velocità con map matching
	avg_speed = insert_speed(points, distance_map_matched_query, insert_speeds_mm_query, cursor, speeds_list)
	print("average speed, map matching = {} m/s = {} km/h".format(avg_speed, avg_speed*3.6))

	connection.commit()

#inserisce nel database le velocità 
def insert_speed(points, distance_query, insert_query, cursor, speeds_list):
	for i, p in enumerate(points[:-1]):
		dt = (points[i+1][1] - points[i][1]).total_seconds()
		data = (points[i][0], points[i+1][0], )
		cursor.execute(distance_query, data)
		ds = 0
		for row in cursor.fetchall():
			ds = row[0]
		speeds_list.append((points[i][0], points[i+1][0], dt, ds))

	speeds_list = list(filter(lambda a: a[3] != 0 and a[2] != 0, speeds_list))

	avg_speed = 0.0
	for i, e in enumerate(speeds_list):
		if e[2] != 0:
			data = (i, e[0], e[1], e[3]/e[2], )
			avg_speed = avg_speed + e[3]/e[2]
			cursor.execute(insert_query, data)

	avg_speed = avg_speed / len(speeds_list)
	return avg_speed