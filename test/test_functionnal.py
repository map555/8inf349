import pytest
from Api8inf349.models import Product
from Api8inf349.url import productURL
from urllib.request import Request, urlopen
from peewee import Select
import json
from Api8inf349.ProductTableInit import CheckExistance_Test, InitializeProduct


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
            Product.create(name=product['name'], type=product['type'],
                           description=product['description'], image=product['image'], height=product['height'],
                           weight=product['weight'], price=product['price'], rating=product['rating'],
                           in_stock=product['in_stock'])

        assert Product.select().count() == 50

def test_CheckExistance(app):
    with app.app_context():
        p = test_product_get_request()
        x = CheckExistance_Test(app, p['products'][0])
        assert x == False

        Product.create(id=p['products'][0]['id'], name=p['products'][0]['name'], type=p['products'][0]['type'],
                       description=p['products'][0]['description'], image=p['products'][0]['image'],
                       height=p['products'][0]['height'], weight=p['products'][0]['weight'],
                       price=p['products'][0]['price'],
                       rating=p['products'][0]['rating'], in_stock=p['products'][0]['in_stock'])

        assert CheckExistance_Test(app, p['products'][0]) == True


class TestRoutes(object):

    def test_index(self, app, client):
        with app.app_context():
            InitializeProduct()

            response = client.get("/")
            assert response.status_code == 200
            jsonResponse = json.loads(response.get_data())
            assert jsonResponse["products"] is not None
            assert len(jsonResponse["products"]) == 50
