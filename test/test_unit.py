from Api8inf349.models import Product, Transaction
from Api8inf349.schemasValidation import *
from getDataSetsForTests import *
from Api8inf349.models import Order, Product
import pytest

"""Because SQLite doesn't force type and peewee doesn't return an error if you try to do weird stuff like
inserting a integer in a charfield, we use the Schema module to validate if the dictionnaries used to 
insert informations in the database respect the structure of the models we define in the models.py file.
The schemas doesn't check the integrity constraints defined in the models because it's the data base's job to do it.
We only validate the structure of the dictionnaries and the data type of their fields. So instead of directly 
individually test each field of each model in little unit tests (because it's useless to do our own assert on each field
when you can still insert invalid stuff in the db outside the context of the tests), we use our validation methods you 
can found in the schemasValidation.py file and we test all the valid case too. Those validation methods return True or
False (the same boolean returned by the is_valid method of a Schema object) depending if the dictionnary is conform to 
the the schema or not. So, for each field, we test individually each wrong case and we did some assert with the boolean
return value to validate if the dict of parameters will instanciate a valid object model or not. So we test our models
by validating the structure of the dictionnaries containing the parameters used to instanciate or inserting informations
in our models and we also reuse those validation methods in the app too."""


# Test if the dictionnary used to instanciate a product object model is valid
@pytest.mark.parametrize("pDict", getInvalidProductDicts())
def test_InvalidProductsDictionnary(pDict):
    assert ValidateProductSchema(pDict) == False


@pytest.mark.parametrize("pDict", getValidProductDict())
def test_ValidProductDictionnary(pDict):
    assert ValidateProductSchema(pDict) == True


# Test if the dictionnary used to instanciate a ShippingInformation object model is valid
@pytest.mark.parametrize("sInfoDict", getInvalidShipInfoDicts())
def test_InvalidShipping(sInfoDict):
    assert ValidateShippingInfoSchema(sInfoDict) == False


@pytest.mark.parametrize("sInfoDict", getValidShipInfoDicts())
def test_ValidShipping(sInfoDict):
    assert ValidateShippingInfoSchema(sInfoDict) == True


@pytest.mark.parametrize("cCardDict", getInvalidCreditCardDicts())
def test_InvalidCreditCardDictionnary(cCardDict):
    assert ValidateCreditCardSchema(cCardDict) == False


@pytest.mark.parametrize("cCardDict", getValidCreditCardDicts())
def test_ValidCreditCardDictionnary(cCardDict):
    assert ValidateCreditCardSchema(cCardDict) == True


@pytest.mark.parametrize("tDict", getInvalidTransactionDicts())
def testInvalidTransactionDictionnary(tDict):
    assert ValidateTransactionSchema(tDict) == False


@pytest.mark.parametrize("tDict", getValidTransactionDicts())
def test_ValidTransactionDictionnary(tDict):
    assert ValidateTransactionSchema(tDict) == True


@pytest.mark.parametrize("oDict", getInvalidOrderDicts())
def test_InvalidOrderDictionnary(oDict):
    assert ValidateOrderSchema(oDict) == False


@pytest.mark.parametrize("oDict", getValidOrderDicts())
def test_ValidOrderDictionnary(oDict):
    assert ValidateOrderSchema(oDict) == True


@pytest.mark.parametrize("pODict", getInvalidProductOrderDicts())
def test_InvalidProductOrderDictionnary(pODict):
    assert ValidateProductOrderSchema(pODict) == False


@pytest.mark.parametrize("pODict", getValidProductOrderDict())
def test_ValidProductOrderDictionnary(pODict):
    assert ValidateProductOrderSchema(pODict) == True


@pytest.mark.parametrize("cInfoDict", getInvalidClientInfoDicts())
def test_InvalidClientInfoDictionnary(cInfoDict):
    assert ValidateClientInfoSchema(cInfoDict) == False


@pytest.mark.parametrize("cInfoDict", getValidClientInfoDict())
def test_ValidClientInfoDictionnary(cInfoDict):
    assert ValidateClientInfoSchema(cInfoDict) == True

def test_set_order_total_price():
    product_price = 200
    product_quantity = 2
    total_price = product_price*product_quantity

    product = Product(id="1", name="product 1", type="type 1", description="description 1", image="image 1", price=product_price)

    order = Order(product=product, product_quantity=product_quantity)

    order.setTotalPrice()

    assert order.total_price == total_price

def test_set_order_shipping_price_with_499g_weight():

    product_price = 200
    product_quantity = 1
    product_weight = 499

    product = Product(id="1", name="product 1", type="type 1", description="description 1", image="image 1",
                      price=product_price, weight=product_weight)

    order = Order(product=product, product_quantity=product_quantity)

    order.setShippingPrice()

    assert order.shipping_price == 5.00

def test_set_order_shipping_price_with_1999g_weight():

    product_price = 200
    product_quantity = 1
    product_weight = 1999

    product = Product(id="1", name="product 1", type="type 1", description="description 1", image="image 1",
                      price=product_price, weight=product_weight)

    order = Order(product=product, product_quantity=product_quantity)

    order.setShippingPrice()

    assert order.shipping_price == 10.00

def test_set_order_shipping_price_with_2001g_weight():

    product_price = 200
    product_quantity = 1
    product_weight = 2001

    product = Product(id="1", name="product 1", type="type 1", description="description 1", image="image 1",
                      price=product_price, weight=product_weight)

    order = Order(product=product, product_quantity=product_quantity)

    order.setShippingPrice()

    assert order.shipping_price == 25.00

