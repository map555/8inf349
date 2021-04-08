import pytest
import json2

from api8inf349 import InitializeProduct, Product
from api8inf349.models import Order, ShippingInformation


class TestOrder(object):
    def test_create_new_order(self, app, client):
        with app.app_context():
            InitializeProduct()

            response = client.post("/order", json={"product": [{"quantity": 1, "id": 1},{"quantity": 1, "id": 2}]})
            assert response.status_code == 302
            assert response.location == "http://localhost/order/1"

            response = client.get("/order/1")
            assert response.status_code == 200
            jsonResponse = json2.loads(response.get_data())
            assert jsonResponse['product']['product_quantity'] == 1
            assert jsonResponse['product']['product_id'] == 1

            response = client.put("/order/1", json={"order": {"email": "firstclient@uqac.ca",
                                                              "shipping_information": {"country": "Canada",
                                                                                       "address": "201, rue des rosiers",
                                                                                       "postal_code": "G7X 3Y9",
                                                                                       "city": "Chicoutimi",
                                                                                       "province": "QC"}}})
            assert response.status_code == 200
            jsonResponse = json2.loads(response.get_data())
            assert jsonResponse['email'] == "firstclient@uqac.ca"
            assert jsonResponse['shipping_information']['country'] == "Canada"
            assert jsonResponse['shipping_information']['address'] == "201, rue des rosiers"
            assert jsonResponse['shipping_information']['postal_code'] == "G7X 3Y9"
            assert jsonResponse['shipping_information']['city'] == "Chicoutimi"
            assert jsonResponse['shipping_information']['province'] == "QC"

            response = client.put("/order/1", json={
                "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                                "cvv": "123", "expiration_month": 9}})
            assert response.status_code == 200
            jsonResponse = json2.loads(response.get_data())
            assert jsonResponse['credit_card']['name'] == 'John Doe'
            assert jsonResponse['credit_card']['number'] == "4242 4242 4242 4242"
            assert jsonResponse['credit_card']['expiration_year'] == 2024
            assert jsonResponse['credit_card']['expiration_month'] == 9
            assert jsonResponse['paid'] is True
            assert jsonResponse['transaction']['id'] is not None
            assert jsonResponse['transaction']['success'] is True
            assert jsonResponse['transaction']['amount_charged'] is not None

    def test_create_order_missing_fields(self, app, client):
        with app.app_context():
            response = client.post("/order", json={"product": {"id": 1}})
            assert response.status_code == 422
            assert b'missing-fields' in response.data

    def test_create_order_invalid_quantity(self, app, client):
        with app.app_context():
            product = Product(name="Brown eggs", type="dairy",
                              description="Raw organic brown eggs in a basket",
                              image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)
            product.save()

            response = client.post("/order", json={"product": {"id": 1, "quantity": -1}})
            assert response.status_code == 422
            assert b'missing-fields' in response.data

    def test_create_order_product_unavailable(self, app, client):
        with app.app_context():
            product = Product(name="Brown eggs", type="dairy",
                              description="Raw organic brown eggs in a basket",
                              image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=False)
            product.save()

            response = client.post("/order", json={"product": {"id": 1, "quantity": 1}})
            assert response.status_code == 422
            assert b'out-of-inventory' in response.data

    def test_credit_card_order_not_found(self, app, client):
        with app.app_context():
            response = client.put("/order/1", json={
                "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                                "cvv": "123", "expiration_month": 9}})

            assert response.status_code == 404
            assert b'not-found' in response.data

    def test_credit_card_missing_client_information(self, app, client):
        with app.app_context():
            product = Product(name="Brown eggs", type="dairy",
                              description="Raw organic brown eggs in a basket",
                              image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=True)

            product.save()

            order = Order(product=product, product_quantity=1)
            order.save()

            response = client.put("/order/1", json={
                "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                                "cvv": "123", "expiration_month": 9}})

            assert response.status_code == 422
            assert b'missing-fields' in response.data

    def test_credit_card_missing_fields(self, app, client):
        with app.app_context():
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

            response = client.put("/order/1", json={
                "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                                "expiration_month": 9}})
            assert response.status_code == 422
            assert b'missing-fields' in response.data

    def test_credit_card_order_already_paid(self, app, client):
        with app.app_context():
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

            response = client.put("/order/1", json={
                "credit_card": {"name": "John Doe", "number": "4242 4242 4242 4242", "expiration_year": 2024,
                                "cvv": "123", "expiration_month": 9}})

            assert response.status_code == 422
            assert b'already-paid' in response.data
