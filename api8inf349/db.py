from redis import Redis
from peewee import PostgresqlDatabase
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
"""
def getDB():
    database = {"host": "localhost", "user": "user", "password": "pass", "port": 5432}
    return database
"""

db=PostgresqlDatabase(url=os.environ["DATABASE_URL"])

def getRedis():
    return Redis.from_url(os.environ["REDIS_URL"])





