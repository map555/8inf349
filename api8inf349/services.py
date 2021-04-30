from api8inf349.models import Product, Order, Transaction, CreditCard, ShippingInformation, ProductOrdered, PaymentError
from api8inf349.schemas_validation import ValidateClientInfoSchema, ValidateProductOrderSchema, \
    ValidateCreditCardOrderSchema
from api8inf349.url import paymentAPIURL
import requests
from api8inf349.db import getRedis
import pickle
from peewee import fn
import json
import click


def getMissingProductFieldErrorDict():
    error = {'errors': {'product': {"code": "", "name": ""}}}
    error['errors']['product']['code'] = "missing-fields"
    error['errors']['product']['name'] = "The creation of an order requires one or more products. " \
                                         "Each order product dictionnary must have the following form:{ 'product': " \
                                         "[{ 'id': id1, 'quantity': quantity1 }, { 'id': id2, 'quantity': quantity2 }]" \
                                         " }. ID and quantity must be integer and quantity > 0."

    dict = {"status_code": 422, "object": error}

    return dict


def getOrderNotFoundErrorDict():
    error = {"errors": {"order": {"code": "", "name": ""}}}
    error['errors']['order']['code'] = "not-found"
    error['errors']['order']['name'] = "Order not found."
    dict = {"status_code": 404, "object": error}

    return dict


def getMissingCreditCardFieldErrorDict():
    error = {"errors": {"credit_card": {"code": "", "name": ""}}}
    error['errors']['credit_card']['code'] = "missing-fields"
    error['errors']['credit_card']['name'] = "The structure of the credit card dict is invalid or there is a least " \
                                             "one missing field."
    dict = {"status_code": 422, "object": error}

    return dict


def getOrderAlreadyPaidErrorDict():
    error = {"errors": {"order": {"code": "", "name": ""}}}
    error['errors']['order']['code'] = "already-paid"
    error['errors']['order']['name'] = "The order has already been paid."

    dict = {"status_code": 422, "object": error}
    return dict


def getAvailabilityProductErrorDict():
    error = {'errors': {'product': {"code": "", "name": ""}}}

    error['errors']['product']['code'] = "out-of-inventory"
    error['errors']['product']['name'] = "The product you asked for is not in the inventory for now."

    dict = {"status_code": 422, "object": error}

    return dict


def getMissingOrderFieldErrorDict():
    error = {"errors": {"order": {"code": "", "name": ""}}}
    error['errors']['order']['code'] = "missing-fields"
    error['errors']['order']['name'] = "Client informations are required before applying a credit card to the order."

    dict = {"status_code": 422, "object": error}

    return dict


def getPaymentApiSError(code, apiResponse, orderModelObject):
    fullOrderDict = createOrderDict(orderModelObject=orderModelObject)

    """
    Dans l'exemple dans l'énoncé du travail, il était question d'un attribut "code".
    Cependant, l'api de paiment ne retourne pas cet attribut. Par conséquent, il n'est pas présent
    dans notre implémentation.
    """
    error = {"name": apiResponse['message']}
    fullOrderDict["object"]['transaction'] = {"success": apiResponse['success'], "error": error, "amount_charged": 0}
    fullOrderDict["status_code"] = code

    # store the error in the database
    p = PaymentError(order=orderModelObject, error=json.dumps(error))
    p.save()
    dbError = PaymentError.get_or_none(PaymentError.order == orderModelObject)
    errorMessage = "id: " + str(dbError.id) + "\torderID: " + str(orderModelObject) + "\terror:\n" + str(
        error) + "\n" + str(dbError.time)
    click.echo(errorMessage)
    return fullOrderDict


def CheckQuantity(pQuantity):
    if pQuantity > 0:
        return True
    else:
        return False


def CheckAvailability(pID):
    p = Product.get_or_none(Product.id == pID)
    if p.in_stock is True:
        return True
    else:
        return False


def createOrderDict(orderModelObject):
    if orderModelObject is None:
        return getOrderNotFoundErrorDict()

    products = ProductOrdered.select(ProductOrdered.product, ProductOrdered.product_quantity).where(
        ProductOrdered.order == orderModelObject)

    pList = []
    for p in products:
        product = {'product_id': p.product.id, 'product_quantity': p.product_quantity}
        pList.append(product)

    orderDict = {'id': orderModelObject.id, 'shipping_information': {}, 'credit_card': {},
                 'email': orderModelObject.email, 'total_price': orderModelObject.total_price, 'transaction': {},
                 'paid': orderModelObject.paid, 'product': pList, 'shipping_price': orderModelObject.shipping_price}

    if orderModelObject.shipping_information is not None:
        orderDict['shipping_information'] = {'country': orderModelObject.shipping_information.country,
                                             'address': orderModelObject.shipping_information.address,
                                             'postal_code': orderModelObject.shipping_information.postal_code,
                                             'city': orderModelObject.shipping_information.city,
                                             'province': orderModelObject.shipping_information.province}

    if orderModelObject.credit_card is not None:
        orderDict['credit_card'] = {'name': orderModelObject.credit_card.name,
                                    'number': orderModelObject.credit_card.number,
                                    'expiration_month': orderModelObject.credit_card.expiration_month,
                                    'expiration_year': orderModelObject.credit_card.expiration_year,
                                    'cvv': orderModelObject.credit_card.cvv}

    if orderModelObject.transaction is not None:
        orderDict['transaction'] = {'id': orderModelObject.transaction.id,
                                    'success': orderModelObject.transaction.success,
                                    'amount_charged': orderModelObject.transaction.amount_charged}

    dict = {"status_code": 200, "object": orderDict}

    return dict


def getMissingFieldErrorDict():
    error = {"errors": {
        "order": {
            "code": "missing-fields",
            "name": "There is a least, one required field missing."
        }
    }}

    dict = {"status_code": 422, "object": error}
    return dict


def ValidateRequiredFieldsForCCard(order):
    productOrdered = ProductOrdered.get_or_none(ProductOrdered.order == order)

    if (((productOrdered is not None) and ((order.email is not None) and (order.shipping_information.id is not None)))
            and ((order.total_price is not None) and (order.shipping_price is not None))):

        return True

    else:
        return False


def ValidateOrder(pList):
    for p in pList:

        if CheckAvailability(p["id"]) is False:
            return getMissingProductFieldErrorDict()

        if CheckQuantity(p["quantity"]) is False:
            return getAvailabilityProductErrorDict()

    return True


# Because we need to get the id we save the order in the data base, we need to get the next ID.
def getNextOrderID():
    id = Order.select(fn.Max(Order.id)).scalar()

    if id is None:
        id = 1
    else:
        id += 1

    return id


class OrderServices(object):

    @classmethod
    def initOrder(cls, data):
        response = {'orderInitialized': False, 'object': None}

        """If all the condition are respected, object will contain the order model object and if at least one condition
        is not respected, object will contain a dict with the first error."""

        if ValidateProductOrderSchema(pOrderDict=data) is True:

            pList = data['product']

            validation = ValidateOrder(pList=pList)

            if validation is not True:
                return validation

            order = Order.create()
            instanciatedProductList = []
            for p in pList:
                prod = ProductOrdered.create(order=order, product=p["id"], product_quantity=p["quantity"])
                instanciatedProductList.append(prod)

            order.setTotalPrice(products=instanciatedProductList)
            order.setShippingPrice(products=instanciatedProductList)
            order.save()

            response['status_code'] = 200
            response['object'] = order.id

        else:
            response = getMissingProductFieldErrorDict()

        return response

    # This method returns the order from the Postgre data base or from redis.
    # If the order is fetched from Postgre, the order is also save to redis at the same time.
    @classmethod
    def getOrder(cls, id):
        redis = getRedis()
        order = redis.get(str(id))

        if order is not None:
            order = pickle.loads(order)

        else:
            order = Order.get_or_none(Order.id == id)

        return order

    @classmethod
    def getOrderDict(cls, id):
        order = cls.getOrder(id)
        return createOrderDict(orderModelObject=order)

    @classmethod
    def setOrderClientInfo(cls, clientInfoDict, orderID):

        o = cls.getOrder(id=orderID)
        if o is not None:

            if not o.paid:

                if ValidateClientInfoSchema(cInfoDict=clientInfoDict) is True:
                    sInfo = clientInfoDict['order']['shipping_information']

                    # Check in the db
                    sInfoModelObject = ShippingInformation.get_or_none(ShippingInformation.address == sInfo[
                        'address'], ShippingInformation.postal_code == sInfo['postal_code'])

                    if sInfoModelObject is None:
                        sInfoModelObject = ShippingInformation.create(country=sInfo['country'],
                                                                      address=sInfo['address'],
                                                                      postal_code=sInfo['postal_code'],
                                                                      city=sInfo['city'], province=sInfo['province'])

                    o.shipping_information = sInfoModelObject.id
                    o.email = clientInfoDict['order']['email']
                    o.save()

                    response = createOrderDict(orderModelObject=o)

                else:
                    response = getMissingFieldErrorDict()

            else:
                response = getOrderAlreadyPaidErrorDict()

        else:
            response = getOrderNotFoundErrorDict()

        return response

    @classmethod
    def setCreditCard(cls, cCardDict, orderId):
        o = cls.getOrder(orderId)

        if o is None:

            response = getOrderNotFoundErrorDict()

        elif o.paid is True:
            response = getOrderAlreadyPaidErrorDict()

        elif ValidateRequiredFieldsForCCard(order=o) is False:
            response = getMissingOrderFieldErrorDict()

        elif ValidateCreditCardOrderSchema(cCardOrderDict=cCardDict) is False:
            response = getMissingCreditCardFieldErrorDict()

        elif not ((len(cCardDict['credit_card']['cvv']) == 3) and (cCardDict['credit_card']['cvv'].isdigit() is True)):
            response = getMissingCreditCardFieldErrorDict()

        else:
            cCardDict["amount_charged"] = o.total_price + o.shipping_price
            paymentAPIResponse = requests.post(url=paymentAPIURL, json=cCardDict)
            statusCode = paymentAPIResponse.status_code
            apiResponseDict = paymentAPIResponse.json()
            if statusCode != 200:
                response = getPaymentApiSError(code=statusCode, apiResponse=apiResponseDict, orderModelObject=o)

            else:

                if "credit_card" in apiResponseDict:

                    cCard = cCardDict["credit_card"]
                    ccModelObject = CreditCard.get_or_none(CreditCard.number == cCard['number'],
                                                           CreditCard.cvv == cCard['cvv'])
                    if ccModelObject is None:
                        ccModelObject = CreditCard(name=cCard['name'], number=cCard['number'],
                                                   expiration_month=cCard['expiration_month'],
                                                   expiration_year=cCard['expiration_year'], cvv=cCard['cvv'])

                    o.credit_card = ccModelObject
                    o.save()

                    t = Transaction.create(id=apiResponseDict['transaction']['id'],
                                           success=apiResponseDict['transaction']['success'],
                                           amount_charged=apiResponseDict['transaction']['amount_charged'])
                    o.transaction = t
                    o.paid = True
                    o.save()

                    redis = getRedis()
                    redis.set(str(o.id), pickle.dumps(o))

                    response = createOrderDict(orderModelObject=o)

                else:
                    '''
                    On ne vérifie pas si le numéro de carte de crédit est 4242 4242 4242 4242 ou 4000 0000 0000 0002 car 
                    ça devrait être l'api distant qui le fait, donc on ne fait que transmettre le message d'erreur de l'api
                    distant au client lorsqu'il y en a un.
                    '''
                    response = getPaymentApiSError(code=statusCode, apiResponse=apiResponseDict, orderModelObject=o)

        return response
