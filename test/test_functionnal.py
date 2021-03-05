import pytest
from Api8inf349.models import Product, Order, ShippingInformation
from Api8inf349.url import productURL
from urllib.request import Request, urlopen
from peewee import Select
import json
from Api8inf349.ProductTableInit import CheckExistance_Test, InitializeProduct
from Api8inf349.services import OrderServices


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


class TestServices(object):

    def test_setCreditCard_order_not_found(self, app):
        response = OrderServices.setCreditCard(cCardDict={
            "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                            "cvv": "123", "expiration_month": 9}},
            orderId=1)

        assert response == {'set': False,
                            "object": {"errors": {"order": {"code": "not-found", "name": "Order not found."}}},
                            "status_code": 404}

    def test_setCreditCard_missing_client_informations(self, app):
        product = Product(name="Brown eggs", type="dairy",
                          description="Raw organic brown eggs in a basket",
                          image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)

        product.save()

        order = Order(product=product, product_quantity=1)
        order.save()

        response = OrderServices.setCreditCard(cCardDict={
            "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                            "cvv": "123", "expiration_month": 9}},
            orderId=1)

        assert response == {'set': False,
                            "object": {"errors": {"order": {"code": "missing-fields",
                                                            "name": "Client informations are required before applying a credit card to the order."}}},
                            "status_code": 422}

    def test_setCreditCard_missing_credit_card_fields(self, app):
        product = Product(name="Brown eggs", type="dairy",
                          description="Raw organic brown eggs in a basket",
                          image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)

        product.save()

        shipping_information = ShippingInformation(country="Canada", address="201, rue des rosiers",
                                                   postal_code="G7X 3Y9", city="Chicoutimi", province="QC")
        shipping_information.save()

        order = Order(product=product, product_quantity=1, email="firstclient@uqac.ca",
                      shipping_information=shipping_information)
        order.setShippingPrice()
        order.setTotalPrice()
        order.save()

        response = OrderServices.setCreditCard(cCardDict={
            "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                            "expiration_month": 9}},
            orderId=1)

        assert response == {'set': False,
                            "object": {"errors": {"credit_card": {"code": "missing-fields",
                                                                  "name": "The structure of the credit card dict is invalid or there is a least " \
                                                                          "one missing field."}}},
                            "status_code": 422}

    def test_setCreditCard_order_already_paid(self, app):
        product = Product(name="Brown eggs", type="dairy",
                          description="Raw organic brown eggs in a basket",
                          image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)

        product.save()

        shipping_information = ShippingInformation(country="Canada", address="201, rue des rosiers",
                                                   postal_code="G7X 3Y9", city="Chicoutimi", province="QC")
        shipping_information.save()

        order = Order(product=product, product_quantity=1, email="firstclient@uqac.ca",
                      shipping_information=shipping_information, paid=True)
        order.setShippingPrice()
        order.setTotalPrice()
        order.save()

        response = OrderServices.setCreditCard(cCardDict={
            "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                            "cvv": "123", "expiration_month": 9}},
            orderId=1)

        assert response == {'set': False,
                            "object": {"errors": {"order": {"code": "already-paid",
                                                            "name": "The order has already been paid."}}},
                            "status_code": 422}

    def test_initOrder_missing_fields(self, app):
        response = OrderServices.initOrder(data={"product": 1})
        assert response == {'orderInitialized': False, 'object': {'errors': {
            'product': {"code": "missing-fields", "name": "The creation of an order requires a single product. " \
                                                          "The product dict must have the following form: { 'product': " \
                                                          "{ 'id': id, 'quantity': quantity } }. Quantity must be an integer > 0."}}}}

    def test_initOrder_product_unavailable(self, app):
        product = Product(name="Brown eggs", type="dairy",
                          description="Raw organic brown eggs in a basket",
                          image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=False)
        product.save()

        response = OrderServices.initOrder(data={"product":{"id": 1, "quantity":1}})
        assert response == {'orderInitialized': False, 'object': {'errors': {
            'product': {"code": "out-of-inventory", "name": "The product you asked for is not in the inventory for now."}}}}

    def test_initOrder_invalid_quantity(self, app):
        product = Product(name="Brown eggs", type="dairy",
                          description="Raw organic brown eggs in a basket",
                          image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)
        product.save()

        response = OrderServices.initOrder(data={"product": {"id": 1, "quantity": -1}})
        assert response == {'orderInitialized': False, 'object': {'errors': {
            'product': {"code": "missing-fields", "name": "The creation of an order requires a single product. " \
                                                          "The product dict must have the following form: { 'product': " \
                                                          "{ 'id': id, 'quantity': quantity } }. Quantity must be an integer > 0."}}}}
