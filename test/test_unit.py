from Api8inf349.models import Product, Transaction
import pytest


class TestProduct:
    def __init__(self, product):
        self.p = product
        assert type(self.p) == Product

    def __test_pk(self):
        assert type(self.p.id) == int

    def __test_name(self):
        assert type(self.p.name) == str
        assert (0 <= len(self.p.name) <= 255)  # because name is a varchar(255) in the database

    def __test_type(self):
        assert type(self.p.type) == str
        assert (0 <= len(self.p.type) <= 255)  # because type is a varchar(255) in the database

    def __test_description(self):
        assert type(self.p.description) == str
        assert (0 <= len(self.p.description) <= 255)  # because description is a varchar(255) in the database

    def __test_image(self):
        assert type(self.p.image) == str
        assert (0 <= len(self.p.image) <= 255)  # because image is a varchar(255) in the database

    def __test_height(self):
        assert type(self.p.height) == int
        assert self.p.height > 0  # Integrity constraint

    def __test_weight(self):
        assert type(self.p.weight) == int
        assert self.p.weight > 0  # Integrity constraint

    def __test_price(self):
        assert type(self.p.price) == float
        assert self.p.price > 0  # Integrity constraint

    def __test_rating(self):
        assert type(self.p.rating) == int
        assert 0 <= self.p.rating <= 5  # Integrity constraints

    def __test_in_stock(self):
        assert type(self.p.in_stock) == bool

    def test_All(self):
        self.__test_pk()
        self.__test_name()
        self.__test_type()
        self.__test_description()
        self.__test_image()
        self.__test_height()
        self.__test_weight()
        self.__test_price()
        self.__test_rating()
        self.__test_in_stock()


# private test?
class TestTransaction:

    def __init__(self, transaction):
        self.__t = transaction
        assert type(self.__t) == Transaction

    def test_pk(self):
        assert type(self.__t.id) == str
        assert (0 <= len(self.__t.id) <= 255)  # because id is a varchar(255) in the database

    def test_success(self):
        assert type(self.__t.success) == bool

    def test_amount_charged(self):
        assert type(self.__t.amount_charged) == float
        # assert self.__t.amount_charged >= 0

    def test_All(self):
        self.test_pk()
        self.test_success()
        self.test_amount_charged()



