#query che ritorna tutti i punti GPS del tragitto
get_points_query = '''SELECT distinct * 
					  FROM tragitto
					  ORDER BY time;'''

delete_tragitto_query = ''' DELETE FROM tragitto'''

insert_points_query = '''INSERT INTO tragitto (id, geom, track_fid, track_seg_id, track_seg_point_id, ele, time) VALUES (%s,%s,%s,%s,%s,%s,%s)'''

#filtra prendendo un punto ogni t secondi
def time_filter(connection, t):
	cursor = connection.cursor()
	cursor.execute(get_points_query)
	points = cursor.fetchall()
	points_filtered = []
	cursor.execute(delete_tragitto_query)
	connection.commit()

	print(len(points))

	dt = 0
	for i, p in enumerate(points[:-1]):
		dt = dt + (points[i+1][6] - points[i][6]).total_seconds()
		if dt > t:
			points_filtered.append(p)
			dt = dt - t

	points_filtered.append(points[-1])


	for e in points_filtered:
		data = (e[0], e[1], e[2], e[3], e[4], e[5], e[6], )
		cursor.execute(insert_points_query, data)
	connection.commit()