import pytest
from Api8inf349.models import Product
from other import productURL
from urllib.request import Request, urlopen
from peewee import Select
import json
from Api8inf349.ProductTableInit import CheckExistance_Test


class TestProduct(object):
    def test_rating(self, app):
        with app.app_context():
            Product.create(id=1, name="Brown eggs", type="dairy", description="Raw organic brown eggs in a basket",
                           image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)

            y = Product.select().count()

            x = 1
            assert x == 1


def getRequest(url):
    r = Request(productURL)
    response = urlopen(r)
    return response


def convertResponseToJson(response):
    jsn = None
    try:
        jsn = json.loads(response.read())
    except Exception as exept:
        print(exept)
    return jsn


def convertProductIdToInt(productsDict):
    for product in productsDict['products']:
        product['id'] = int(product['int'])

    return productsDict


def test_product_get_request():
    response = getRequest(url=productURL)
    assert response.getcode() == 200  # Check if the request return the http 200 status code

    jsn = convertResponseToJson(response=response)
    assert type(jsn) == dict  # Check if the response is converted to json dict successfully

    return jsn


def test_load_product_db(app):
    with app.app_context():
        products = test_product_get_request()

        for product in products['products']:
            Product.create(id=int(product['id']), name=product['name'], type=product['type'],
                           description=product['description'], image=product['image'], height=product['height'],
                           weight=product['weight'], price=product['price'], rating=product['rating'],
                           in_stock=product['in_stock'])

        assert Product.select().count() == 50



def test_CheckExistance(app):
    with app.app_context():
        p = test_product_get_request()
        x= CheckExistance_Test(app, p['products'][0])
        assert x == False

        Product.create(id=p['products'][0]['id'], name=p['products'][0]['name'], type=p['products'][0]['type'],
                       description=p['products'][0]['description'], image=p['products'][0]['image'],
                       height=p['products'][0]['height'], weight=p['products'][0]['weight'],
                       price=p['products'][0]['price'],
                       rating=p['products'][0]['rating'], in_stock=p['products'][0]['in_stock'])

        assert CheckExistance_Test(app, p['products'][0]) == True
