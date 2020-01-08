import psycopg2
from itertools import cycle

#ritorna tutti i punti del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto
					  ORDER BY time;'''

#cancella tutti i punti dalla tabella delle velocità
delete_speed_query = '''DELETE FROM speed'''

#calcola la distanza tra due punti
distance_query = '''SELECT st_distance(p1.geom::geography, p2.geom::geography)
					FROM tragitto as p1, tragitto as p2
					WHERE p1.id = %s AND p2.id = %s'''

#inserisce le velocità calcolate nella tabella speed
insert_speeds_query = '''INSERT INTO speed 
				   VALUES (%s, %s, %s, %s)''' #id idp1 idp2 speed

def calc_speed(connection):
	cursor = connection.cursor()

	#lista di tuple(id_p1, id_p2, Δt, Δs)
	speeds_list = []

	cursor.execute(delete_speed_query)
	connection.commit()

	cursor.execute(get_points_query)

	points = cursor.fetchall()

	for i, p in enumerate(points[:-1]):
		dt = (points[i+1][6] - points[i][6]).total_seconds()
		data = (points[i][0], points[i+1][0], )
		cursor.execute(distance_query, data)
		ds = 0
		for row in cursor.fetchall():
			ds = row[0]
		speeds_list.append((points[i][0], points[i+1][0], dt, ds))

	avg_speed = 0
	for i, e in enumerate(speeds_list):
		data = (i, e[0], e[1], e[3]/e[2], )
		avg_speed = avg_speed + e[3]/e[2]
		cursor.execute(insert_speeds_query, data)

	avg_speed = avg_speed / len(speeds_list)
	print("average speed = {} m/s = {} km/h".format(avg_speed, avg_speed*3.6))

	connection.commit()