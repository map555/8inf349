import os
from peewee import PostgresqlDatabase
import psycopg2
from peewee import Model, AutoField, CharField, ForeignKeyField, IntegerField, FloatField, PostgresqlDatabase, \
    BooleanField, \
    Check
# con=psycopg2.connect(database="api8inf349", host="localhost", user="user", password="pass")
# db=PostgresqlDatabase("api8inf349", host="localhost", user="user", password="pass",port=5432)

# db = PostgresqlDatabase(database=os.environ["DB_NAME"], host=os.environ["DB_HOST"], port=os.environ["DB_PORT"],
#                        user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"])

def getDB():
    database = {"host": "localhost", "user": "user", "password": "pass", "port": 5432}
    return database




conn = psycopg2.connect(database="api8inf349", **getDB())
cursor=conn.cursor()
cursor.execute("SELECT * FROM product")
records=cursor.fetchall()
for r in records:
    print(r)
print("\n\n")
cursor.execute("SELECT * FROM product WHERE id=1")
records=cursor.fetchall()
print(records)
conn.close()
