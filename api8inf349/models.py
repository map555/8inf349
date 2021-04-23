import json
import os
from urllib.request import Request, urlopen
import click
from flask.cli import with_appcontext
from peewee import Model, TextField, TimestampField, AutoField, CharField, ForeignKeyField, IntegerField, FloatField, \
    BooleanField, PostgresqlDatabase, Check
from api8inf349.schemas_validation import ValidateProductListSchema
from api8inf349.url import productURL
from api8inf349.db import getDB

# FLASK_DEBUG=True FLASK_APP=Api8inf349 REDIS_URL=redis://localhost DB_HOST=localhost DB_USER=user DB_PASSWORD=pass DB_PORT=5432 DB_NAME=api8inf349 flask init-db
# set FLASK_DEBUG=True& set FLASK_APP=api8inf349& set REDIS_URL=redis://localhost& set DB_HOST=localhost& set DB_USER=user& set DB_PASSWORD=pass& set DB_PORT=5432& set DB_NAME=api8inf349
# docker run -p 5000:5000 -e REDIS_URL=redis://host.docker.internal -e DB_HOST=host.docker.internal -e DB_USER=user -e DB_PASSWORD=pass -e DB_PORT=5432 -e DB_NAME=api8inf349 api8inf349







class BaseModel(Model):
    class Meta:
        database = getDB()


class Product(BaseModel):
    id = AutoField(primary_key=True, null=False)
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
    id = AutoField(primary_key=True)
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
    amount_charged = FloatField(null=True)

    def __str__(self):
        return self.id


class Order(BaseModel):
    id = AutoField(primary_key=True)
    shipping_information = ForeignKeyField(ShippingInformation, null=True, default=None)
    credit_card = ForeignKeyField(CreditCard, null=True, default=None)
    email = CharField(null=True, default=None)
    total_price = FloatField(null=True, default=None, constraints=[Check('total_price>0')])
    transaction = ForeignKeyField(Transaction, null=True, default=None)
    paid = BooleanField(null=False, default=False)
    shipping_price = FloatField(null=True, constraints=[Check('shipping_price>=0')])

    def setTotalPrice(self, products):

        sum = 0
        for p in products:
            sum += (p.product.price * p.product_quantity)

        self.total_price = sum

    def setShippingPrice(self, products):
        totalWeight = 0
        for p in products:
            totalWeight += (p.product.weight * p.product_quantity)

        if totalWeight < 500:
            self.shipping_price = 5.00
        elif totalWeight < 2000:
            self.shipping_price = 10.00
        else:
            self.shipping_price = 25.00


class ProductOrdered(BaseModel):
    id = AutoField(primary_key=True)
    order = ForeignKeyField(Order, null=False)
    product = ForeignKeyField(Product, null=False)
    product_quantity = IntegerField(null=False)


class PaymentError(BaseModel):
    id = AutoField(primary_key=True)
    order = ForeignKeyField(Order, null=False)
    error = TextField(null=False)
    time = TimestampField()



def getRequest(url):
    r = Request(productURL)
    response = urlopen(r)
    code = response.getcode()
    if code != 200:
        print("ERROR: trying to get products from \"http://jgnault.ddns.net/shops/products/\" return http code", code)
        exit(0)
    return response


def ConvertResponseToJson(response):
    jsn = None
    try:
        jsn = json.loads(response.read())
    except Exception as exept:
        print(exept)
    # fix the problem with the null char for product id 45
    jsn['products'][44][
        'description'] = "Healthy breakfast set. rice cereal or porridge with fresh strawberry, apricots," \
                         "almond and honey over white rustic wood backdrop, top view."

    return jsn


def getProducts():
    response = getRequest(url=productURL)
    jsonDict = ConvertResponseToJson(response=response)
    return jsonDict


def CheckExistance(jsonProduct):
    id = int(jsonProduct['id'])

    try:
        query = Product.get_or_none(Product.id == id)
        if query is not None:
            return True
        else:
            return False
    except:
        return False


# we dont test this one because CheckExistance and bd insert are already tested.
def UpdateProduct(ProductsDict):
    if ValidateProductListSchema(ProductsDict) is False:
        print("ERROR: INVALID PRODUCT!\nTHE PROGRAM WILL NOW EXIT.")
        exit(0)
    for p in ProductsDict['products']:
        checkExist = CheckExistance(p)
        if checkExist is not True:
            Product.create(name=p['name'], type=p['type'], description=p['description'], image=p['image'],
                           height=p['height'], weight=p['weight'], price=p['price'], rating=p['rating'],
                           in_stock=p['in_stock'])


def InitializeProduct():
    products = getProducts()
    UpdateProduct(ProductsDict=products)  # check if update




@click.command("init-db")
@with_appcontext
def init_db_command():
    db = getDB()
    db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order, ProductOrdered, PaymentError])
    InitializeProduct()
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)

