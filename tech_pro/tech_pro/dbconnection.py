import psycopg2
import os
def connection():
    db = f"dbname={os.getenv('DATABASE')} user={os.getenv('USER')} password={os.getenv('PASSWORD')} host={os.getenv('HOST')}"

    conn = psycopg2.connect(db)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS festusers(name VARCHAR(50) NOT NULL,clg_name VARCHAR(50) NOT NULL,email VARCHAR(50) NOT NULL,event VARCHAR(50) NOT NULL,branch VARCHAR(50) NOT NULL);")
    c.execute("CREATE TABLE IF NOT EXISTS admin(email VARCHAR(50) NOT NULL,password VARCHAR(100) NOT NULL);")
    c.execute("INSERT INTO admin(email,password) VALUES('grsssmurthy@gmail.com','$5$rounds=535000$9YL1aEvAnQf8xkqX$8KrRBUeuqlDMEVfUWU2AbLRt1lZC49XB0P1fV8CPupB');")
    return c, conn