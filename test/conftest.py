import os

os.environ['DATABASE'] = ":memory:"
import pytest
from peewee import SqliteDatabase
from Api8inf349 import create_app
from Api8inf349.models import get_db_path, Product, ShippingInformation, CreditCard, Transaction, Order


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    db = SqliteDatabase(get_db_path())
    db.create_tables([Product, ShippingInformation, CreditCard, Transaction, Order])

    yield app

    db.drop_tables([Product, ShippingInformation, CreditCard, Transaction, Order])
