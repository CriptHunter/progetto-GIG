import psycopg2
import map_matching
import speed

try:
	connection = psycopg2.connect(user = "postgres",
								  password = "morris96",
								  host = "127.0.0.1",
								  port = "5432",
								  database = "consegna5")

	cursor = connection.cursor()
	print("Connected to DB")

	map_matching.match(connection)
	speed.calc_speed(connection)

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)

finally:
	if(connection):
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed")