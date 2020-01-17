for row in points:
		point_id = row[4]
		data = (point_id, )
		cursor.execute(get_closest_line_query, data)
		closest_line_id = cursor.fetchall()
		for row in closest_line_id:
			closest_line_id = row[0]
		point_closest_line_list.append((point_id, closest_line_id))