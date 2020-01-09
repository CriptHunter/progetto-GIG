import psycopg2
import map_matching
import speed
import filtering

copy_tragitto_query = ''' INSERT INTO tragitto_filtered (id, geom, track_fid, track_seg_id, track_seg_point_id, ele, time)
						  SELECT id, geom, track_fid, track_seg_id, track_seg_point_id, ele, time
						  FROM tragitto'''

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "morris96",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "consegna5")

	cursor = connection.cursor()
	print("Connected to DataBase")

	cursor.execute(filtering.delete_tragittof_query)
	cursor.execute(copy_tragitto_query)
	connection.commit()

	map_matching.match(connection)
	speed.avg_speed(connection)

	filtering.time_filter(connection, 3)

	map_matching.match(connection)
	speed.avg_speed(connection)


except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)

finally:
	if(connection):
		print('-'*100)
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")