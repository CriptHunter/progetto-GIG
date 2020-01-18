speeds_list = list(filter(lambda a: a[3] != 0 and 
                            a[2] != 0, speeds_list))
for i, e in enumerate(speeds_list):
	if e[2] != 0:
		data = (i, e[0], e[1], e[3]/e[2], )
		avg_speed = avg_speed + e[3]/e[2]
		cursor.execute(insert_query, data)
avg_speed = avg_speed / len(speeds_list)