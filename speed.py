import psycopg2
from itertools import cycle

#ritorna tutti i punti del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto
					  ORDER BY time;'''

delete_speed_query = '''DELETE FROM speed'''

distance_query = '''SELECT st_distance(p1.geom::geography, p2.geom::geography)
					FROM tragitto as p1, tragitto as p2
					WHERE p1.id = %s AND p2.id = %s'''

insert_speeds_query = '''INSERT INTO speed 
				   VALUES (%s, %s, %s, %s)''' #id idp1 idp2 speed

speeds_list = [] #id1 id2 dt ds

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "morris96",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "consegna5")

	cursor = connection.cursor()
	print("You are connected")

	cursor.execute(delete_speed_query)
	cursor.execute(get_points_query)

	points = cursor.fetchall() #ritorna array di punti

	for i, p in enumerate(points[:-1]):
		dt = (points[i+1][6] - points[i][6]).total_seconds()
		data = (points[i][0], points[i+1][0], )
		cursor.execute(distance_query, data)
		ds = 0
		for row in cursor.fetchall():
			ds = row[0]
		speeds_list.append((points[i][0], points[i+1][0], dt, ds))

	for i, e in enumerate(speeds_list):
		data = (i, e[0], e[1], e[3]/e[2], )
		cursor.execute(insert_speeds_query, data)

	connection.commit()


except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)

finally:
	#closing database connection
	if(connection):
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")