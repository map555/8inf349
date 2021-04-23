from redis import Redis
import os
from peewee import PostgresqlDatabase
import psycopg2
from peewee import Model, AutoField, CharField, ForeignKeyField, IntegerField, FloatField, PostgresqlDatabase, \
    BooleanField, \
    Check


def getDBParameters():
    return {"host": os.environ["DB_HOST"], "user": os.environ["DB_USER"], "password": os.environ["DB_PASSWORD"],
            "port": os.environ["DB_PORT"]}

def getDB():
    return PostgresqlDatabase(os.environ["DB_NAME"], **getDBParameters())

def getRedis():
    return Redis.from_url(os.environ["REDIS_URL"])




