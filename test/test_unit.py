from Api8inf349.models import Product, Transaction
from Api8inf349.schemasValidation import *
from getDataSetsForTests import *
from Api8inf349.models import Order, Product
import pytest


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


@pytest.mark.parametrize("pbODict", getInvalidBasicProductOrderDict())
def test_InvalidProductBasicOrderDictionnary(pbODict):
    assert ValidateBasicProductOrderSchema(pbODict) == False


@pytest.mark.parametrize("pbODict", getValidBasicProductOrderDict())
def test_ValidProductBasicOrderDictionnary(pbODict):
    assert ValidateBasicProductOrderSchema(pbODict) == True

@pytest.mark.parametrize("cInfoDict", getInvalidClientInfoDicts())
def test_InvalidClientInfoDictionnary(cInfoDict):
    assert ValidateClientInfoSchema(cInfoDict) == False


@pytest.mark.parametrize("cInfoDict", getValidClientInfoDict())
def test_ValidClientInfoDictionnary(cInfoDict):
    assert ValidateClientInfoSchema(cInfoDict) == True


def test_set_order_total_price():
    product_price = 200
    product_quantity = 2
    total_price = product_price * product_quantity

    product = Product(id="1", name="product 1", type="type 1", description="description 1", image="image 1",
                      price=product_price)

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
