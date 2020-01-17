	for elem in point_closest_line_list:
		data = (elem[1], elem[0])
		cursor.execute(point_match_query, data)
		matched_point = cursor.fetchall()
		for row in matched_point:
			data = (k, row[0], elem[0])
			cursor.execute('''INSERT INTO matched_point (id, geom, track_seg_point_id) VALUES (%s, %s, %s)''', data)
		k = k + 1