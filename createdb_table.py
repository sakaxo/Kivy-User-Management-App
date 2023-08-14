import psycopg2

conn = psycopg2.connect(database = "kvappdb", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")

print("Opened database successfully")

cur = conn.cursor()

cur.execute(""" CREATE TABLE MYUSER(
	ID SERIAL PRIMARY KEY,
	first_name VARCHAR(100)  NOT NULL,
	last_name VARCHAR(100)  NOT NULL,
	email VARCHAR(255) UNIQUE  NOT NULL,	 
	phone VARCHAR(10)  UNIQUE NOT NULL,
	password TEXT  NOT NULL

);""")


print("Table created successfully")

conn.commit()
conn.close()

