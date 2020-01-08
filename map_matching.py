#query che trova la strada più vicina ad un punto
get_closest_line_query = '''SELECT strade.osm_id
						 FROM tragitto, strade_open_street_map as strade 
						 WHERE tragitto.track_seg_point_id = %s
						 ORDER BY st_distance(tragitto.geom, strade.geom) 
						 LIMIT 1;'''

#query che proietta un punto sulla linea più vicina
point_match_query = '''SELECT st_closestpoint(strade.geom, tragitto.geom)
						  FROM strade_open_street_map as strade, tragitto as tragitto
						  WHERE CAST(strade.osm_id AS int) = %s AND tragitto.track_seg_point_id = %s;'''

#query che ritorna tutti i punti GPS del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto
					  ORDER BY time;'''

#query che cancella tutti i punti generati dal map maptching
delete_points_query = '''DELETE FROM matched_point'''

def fix_isolated_point(point_closest_line_list):
	k = 1
	for elem in point_closest_line_list[1:-1]:
		if point_closest_line_list[k-1][1] == point_closest_line_list[k+1][1]:
			point_closest_line_list[k] = (point_closest_line_list[k][0], point_closest_line_list[k+1][1])
		k = k + 1
	return point_closest_line_list

def match(connection):
	cursor = connection.cursor()
	cursor.execute(delete_points_query)
	connection.commit()

	cursor.execute(get_points_query)

	#lista di tuple (point, closest_line)
	point_closest_line_list = []

	#trovo linea più vicina al punto
	points = cursor.fetchall()
	for row in points:
		point_id = row[4]
		data = (point_id, )
		cursor.execute(get_closest_line_query, data)
		closest_line_id = cursor.fetchall()
		for row in closest_line_id:
			closest_line_id = row[0]
		point_closest_line_list.append((point_id, closest_line_id))
	print("found closest lines")

	point_closest_line_list = fix_isolated_point(point_closest_line_list)

	#trovo punto sulla linea
	for elem in point_closest_line_list:
		data = (elem[1], elem[0])
		cursor.execute(point_match_query, data)
		matched_point = cursor.fetchall()
		for row in matched_point:
			cursor.execute('''INSERT INTO matched_point (id, geom) VALUES (%s, %s)''', (elem[0],(row[0],)))
	print("map matched points")

	connection.commit()
