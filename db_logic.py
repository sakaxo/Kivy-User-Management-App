import psycopg2

def do_registration(first_name,last_name,phone_number,email,password):
 
  conn = psycopg2.connect(database = "kvappdb", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")

  cur = conn.cursor()

  cur.execute("INSERT INTO MYUSER(first_name,last_name,email,phone,password) VALUES (%s,%s,%s,%s,%s);",
    (first_name,last_name,email,phone_number,password))


  conn.commit()
  conn.close()










