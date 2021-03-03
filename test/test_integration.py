import pytest
import json

from Api8inf349 import InitializeProduct


class TestOrder(object):
    def test_create_new_order(self, app, client):
        with app.app_context():
            InitializeProduct()

            response = client.post("/order", json={"product": {"quantity": 1, "id": 1}})
            assert response.status_code == 302
            assert response.location == "http://localhost/order/1"

            response = client.get("/order/1")
            assert response.status_code == 200
            jsonResponse = json.loads(response.get_data())
            assert jsonResponse['product']['product_quantity'] == 1
            assert jsonResponse['product']['product_id'] == 1

            response = client.put("/order/1", json={"order": {"email": "firstclient@uqac.ca",
                                                              "shipping_information": {"country": "Canada",
                                                                                       "address": "201, rue des rosiers",
                                                                                       "postal_code": "G7X 3Y9",
                                                                                       "city": "Chicoutimi",
                                                                                       "province": "QC"}}})
            assert response.status_code == 200
            jsonResponse = json.loads(response.get_data())
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
            jsonResponse = json.loads(response.get_data())
            assert jsonResponse['credit_card']['name'] == 'John Doe'
            assert jsonResponse['credit_card']['number'] == "4242 4242 4242 4242"
            assert jsonResponse['credit_card']['expiration_year'] == 2024
            assert jsonResponse['credit_card']['expiration_month'] == 9
            assert jsonResponse['paid'] is True
            assert jsonResponse['transaction']['id'] is not None
            assert jsonResponse['transaction']['success'] is True
            assert jsonResponse['transaction']['amount_charged'] is not None
