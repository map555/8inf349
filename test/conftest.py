import os
import pytest
from api8inf349.db import getDB
from api8inf349 import create_app
from api8inf349.models import get_db_path, Product, ShippingInformation, CreditCard, Transaction, Order,\
    ProductOrdered, PaymentError
os.environ['DATABASE'] = ":memory:"

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    db = getDB()
    db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order, ProductOrdered, PaymentError])

    yield app

    db.drop_tables([Product, ShippingInformation, CreditCard, Transaction, Order, ProductOrdered, PaymentError])
