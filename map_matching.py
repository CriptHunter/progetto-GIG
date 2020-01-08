import psycopg2

def fix_isolated_point(point_closest_line_list):
	k = 1
	for elem in point_closest_line_list[1:-1]:
		if point_closest_line_list[k-1][1] == point_closest_line_list[k+1][1]:
			print("fix punto " + str(elem[0]))
			point_closest_line_list[k] = (point_closest_line_list[k][0], point_closest_line_list[k+1][1])
		k = k + 1
	return point_closest_line_list

#genera una query che trova la linea più vicina ad un punto con id point_id
def get_closest_line_factory(point_id):
	get_closest_line = '''SELECT strade.osm_id
						 FROM tragitto, strade_open_street_map as strade 
						 WHERE tragitto.track_seg_point_id = {}
						 ORDER BY st_distance(tragitto.geom, strade.geom) 
						 LIMIT 1;'''.format(point_id)
	return get_closest_line

#genera una query che proietta il punto sulla linea più vicina
def point_match_factory(point_id, line_id):
	point_match = '''SELECT st_closestpoint(strade.geom, tragitto.geom)
						  FROM strade_open_street_map as strade, tragitto as tragitto
						  WHERE CAST(strade.osm_id AS int) = {} AND tragitto.track_seg_point_id = {};'''.format(line_id, point_id)
	return point_match


#ritorna tutti i punti del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto
					  ORDER BY time;'''

delete_points_query = '''DELETE FROM matched_point'''

point_closest_line_list = []

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "morris96",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "consegna5")

	cursor = connection.cursor()
	print("You are connected")

	cursor.execute(delete_points_query)
	cursor.execute(get_points_query)

	points = cursor.fetchall() #ritorna array di punti
	for row in points:
		#trovo linea più vicina al punto
		point_id = row[4]
		cursor.execute(get_closest_line_factory(point_id))
		closest_line_id = cursor.fetchall()
		for row in closest_line_id:
			closest_line_id = row[0]

		point_closest_line_list.append((point_id, closest_line_id))


	for e in point_closest_line_list:
		print(e)

	point_closest_line_list = fix_isolated_point(point_closest_line_list)

	for elem in point_closest_line_list:
		#trovo punto sulla linea
		cursor.execute(point_match_factory(elem[0], elem[1]))
		matched_point = cursor.fetchall()
		for row in matched_point:
			cursor.execute('''INSERT INTO matched_point (id, geom) VALUES (%s, %s)''', (elem[0],(row[0],)))

	connection.commit()

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)

finally:
	#closing database connection
	if(connection):
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")