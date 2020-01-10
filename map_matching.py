#query che trova la strada più vicina ad un punto
get_closest_line_query = '''SELECT strade.osm_id
						 	FROM tragitto_filtered as t, strade_open_street_map as strade 
						 	WHERE t.track_seg_point_id = %s AND
						 	strade.highway <> 'pedestrian' AND strade.highway <> 'footway'
						 	ORDER BY st_distance(t.geom, strade.geom) 
						 	LIMIT 1;'''

#query che proietta un punto sulla linea più vicina
point_match_query = '''SELECT st_closestpoint(strade.geom, t.geom)
					   FROM strade_open_street_map as strade, tragitto_filtered as t
					   WHERE CAST(strade.osm_id AS int) = %s AND t.track_seg_point_id = %s;'''

#query che ritorna tutti i punti GPS del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto_filtered
					  ORDER BY time;'''

#query che cancella tutti i punti generati dal map maptching
delete_points_query = '''DELETE FROM matched_point'''

def fix_isolated_point(plist):
	k = 1
	for elem in plist[1:-1]:
		if plist[k-1][1] == plist[k+1][1]:
			plist[k] = (plist[k][0], plist[k+1][1])
		elif plist[k-1][1] != elem[1] and elem[1] != plist[k+1][1]:
			plist[k] = (plist[k][0], plist[k+1][1])
		k = k + 1
	return plist

def match(connection):
	print('-'*100)
	print("MAP MATCHING:")
	cursor = connection.cursor()
	cursor.execute(delete_points_query)
	connection.commit()

	cursor.execute(get_points_query)

	#lista di tuple (point, closest_line)
	point_closest_line_list = []

	#trovo linea più vicina al punto
	points = cursor.fetchall()
	print("Number of points: {}".format(len(points)))
	for row in points:
		point_id = row[4]
		data = (point_id, )
		cursor.execute(get_closest_line_query, data)
		closest_line_id = cursor.fetchall()
		for row in closest_line_id:
			closest_line_id = row[0]
		point_closest_line_list.append((point_id, closest_line_id))
	print("found closest lines...")

	point_closest_line_list = fix_isolated_point(point_closest_line_list)

	#trovo punto sulla linea
	k = 1
	for elem in point_closest_line_list:
		data = (elem[1], elem[0])
		cursor.execute(point_match_query, data)
		matched_point = cursor.fetchall()
		for row in matched_point:
			data = (k, row[0], elem[0])
			cursor.execute('''INSERT INTO matched_point (id, geom, track_seg_point_id) VALUES (%s, %s, %s)''', data)
		k = k + 1
	print("map matched points")

	connection.commit()
