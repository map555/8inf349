import os
import click
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, AutoField, CharField, ForeignKeyField, IntegerField, FloatField, BooleanField


def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())


class Product(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    type = CharField()
    description = CharField()
    image = CharField()
    height = IntegerField(constraints=['height > 0'])
    weight = IntegerField(constraints=['weight > 0'])
    price = FloatField(constraints=['price > 0'])
    rating = IntegerField(constraints=['rating >=0', 'rating <=5'])
    in_stock = BooleanField()

class ShippingInformation(BaseModel):
    id=AutoField(primary_key=True)
    country=CharField()
    address=CharField()
    postal_code=CharField()
    city=CharField()
    province=CharField()

class CreditCard(BaseModel):
    id=AutoField(primary_key=True)
    name=CharField()
    number=CharField()
    expirationMonth=IntegerField()
    expirationYear=IntegerField()
    cvv=IntegerField()

class Transaction(BaseModel):
    id=CharField(primary_key=True)
    success=BooleanField()
    amount_charged=FloatField()

@click.command("init-db")
@with_appcontext
def init_db_command():
    database=SqliteDatabase(get_db_path())
    database.create_tables([Product])
    click.echo("Initialized the database.")

def init_app(app):
    app.cli.add_command(init_db_command)
