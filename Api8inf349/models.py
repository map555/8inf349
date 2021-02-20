import os
import click
from flask.cli import with_appcontext
from peewee import Model, SqliteDatabase, AutoField, CharField, ForeignKeyField, IntegerField, FloatField, BooleanField, \
    Check


def get_db_path():
    return os.environ.get('DATABASE', './db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase(get_db_path())


class Product(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    name = CharField(null=False)
    type = CharField(null=False)
    description = CharField(null=False)
    image = CharField(null=False)
    height = IntegerField(null=False, constraints=[Check('height>0')])
    weight = IntegerField(null=False, constraints=[Check('weight>0')])
    price = FloatField(null=False, constraints=[Check('price>0')])
    rating = IntegerField(null=False, constraints=[Check('rating>=0'), Check('rating<=5')])
    in_stock = BooleanField(null=False)

    def __str__(self):
        return self.id


class ShippingInformation(BaseModel):
    id = AutoField(primary_key=True) # We don't need to test this field because it's an autoincremented field.
    country = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    province = CharField()

    def __str__(self):
        return self.id


class CreditCard(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    number = CharField()
    expiration_month = IntegerField()
    expiration_year = IntegerField()
    cvv = IntegerField()

    def __str__(self):
        return self.id


class Transaction(BaseModel):
    id = CharField(primary_key=True)
    success = BooleanField()
    amount_charged = FloatField()

    def __str__(self):
        return self.id


class Order(BaseModel):
    id = AutoField(primary_key=True)
    shipping_information = ForeignKeyField(ShippingInformation, backref="orders", null=True, default=None)
    credit_card = ForeignKeyField(CreditCard, backref="orders", null=True, default=None)
    email = CharField(null=True, default=None)
    total_price = FloatField(null=True, default=None, constraints=[Check('total_price>0')])
    transaction = ForeignKeyField(Transaction, backref="orders", null=True, default=None)
    paid = BooleanField(null=False, default=False)
    product = ForeignKeyField(Product, backref="orders", null=False)
    product_quantity = IntegerField(null=False)
    shipping_price = FloatField(null=True, constraints=[Check('shipping_price>=0')])


@click.command("init-db")
@with_appcontext
def init_db_command():
    database = SqliteDatabase(get_db_path())
    database.create_tables([Product, ShippingInformation, CreditCard, Transaction,Order])
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)


