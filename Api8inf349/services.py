from Api8inf349.models import Product, Order, Transaction, CreditCard, ShippingInformation
from peewee import DoesNotExist
from Api8inf349.schemas import ClientInfoSchema
from Api8inf349.schemasValidation import ValidateClientInfoSchema, ValidateProductOrderSchema, \
    ValidateCreditCardOrderSchema
from Api8inf349.url import paymentAPIURL
import requests


def getMissingProductFieldErrorDict():
    dict = {'errors': {'product': {"code": "", "name": ""}}}
    dict['errors']['product']['code'] = "missing-fields"
    dict['errors']['product']['name'] = "The creation of an order requires a single product. " \
                                        "The product dict must have the following form: { 'product': " \
                                        "{ 'id': id, 'quantity': quantity } }. Quantity must be an integer > 0."

    return dict


def getOrderNotFoundErrorDict():
    dict = {"errors": {"order": {"code": "", "name": ""}}}
    dict['errors']['order']['code'] = "not-found"
    dict['errors']['order']['name'] = "Order not found."
    return dict


def getMissingCreditCardFieldErrorDict():
    dict = {"errors": {"credit_card": {"code": "", "name": ""}}}
    dict['errors']['credit_card']['code'] = "missing-fields"
    dict['errors']['credit_card']['name'] = "The structure of the credit card dict is invalid or there is a least " \
                                            "one missing field."
    return dict


def getCreditCardDeclinedErrorDict(apiResponse):
    dict = {"errors": {"credit_card": {"code": "", "payment_API_Response": ""}}}
    dict['errors']['credit_card']['code'] = "card-declined"
    dict['errors']['credit_card']['payment_API_Response'] = apiResponse
    return dict


def getOrderAlreadyPaidErrorDict():
    dict = {"errors": {"order": {"code": "", "name": ""}}}
    dict['errors']['order']['code'] = "already-paid"
    dict['errors']['order']['name'] = "The order has already been paid."
    return dict


def getAvailabilityProductErrorDict():
    dict = {'errors': {'product': {"code": "", "name": ""}}}

    dict['errors']['product']['code'] = "out-of-inventory"
    dict['errors']['product']['name'] = "The product you asked for is not in the inventory for now."

    return dict


def getMissingOrderFieldErrorDict():
    dict = {"errors": {"order": {"code": "", "name": ""}}}
    dict['errors']['order']['code'] = "missing-fields"
    dict['errors']['order']['name'] = "Client informations are required before applying a credit card to the order."

    return dict


def getPaymentApiStatusCodeError(statusCode):
    dict = {"errors": {"payment_API": {"code": "", "name": ""}}}
    dict['errors']['payment_API']['code'] = "Paymen API status code"
    dict['errors']['payment_API']['name'] = "Payment API returned HTTP status code " + str(statusCode) + "."
    return dict


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
    orderDict = {'id': orderModelObject.id, 'shipping_information': {}, 'credit_card': {},
                 'email': orderModelObject.email, 'total_price': orderModelObject.total_price, 'transaction': {},
                 'paid': orderModelObject.paid, 'product': {'product_id': orderModelObject.product.id,
                                                            'product_quantity': orderModelObject.product_quantity},
                 'shipping_price':
                     orderModelObject.shipping_price}

    if orderModelObject.shipping_information is not None:
        orderDict['shipping_information'] = {'id': orderModelObject.shipping_information.id,
                                             'country': orderModelObject.shipping_information.country,
                                             'address': orderModelObject.shipping_information.address,
                                             'postal_code': orderModelObject.shipping_information.postal_code,
                                             'city': orderModelObject.shipping_information.city,
                                             'province': orderModelObject.shipping_information.province}

    if orderModelObject.credit_card is not None:
        orderDict['credit_card'] = {'id': orderModelObject.credit_card.id, 'name': orderModelObject.credit_card.name,
                                    'number': orderModelObject.credit_card.number,
                                    'expiration_month': orderModelObject.credit_card.expiration_month,
                                    'expiration_year': orderModelObject.credit_card.expiration_year,
                                    'cvv': orderModelObject.credit_card.cvv}

    if orderModelObject.transaction is not None:
        orderDict['transaction'] = {'id': orderModelObject.transaction.id,
                                    'success': orderModelObject.transaction.success,
                                    'amount_charged': orderModelObject.transaction.amount_charged}

    return orderDict


def getMissingFieldErrorDict():
    errorDict = {"errors": {
        "order": {
            "code": "missing-fields",
            "name": "There is a least, one required field missing."
        }
    }}
    return errorDict


def ValidateRequiredFieldsForCCard(order):
    if ((((order.product.id is not None) and (order.product_quantity is not None)) and ((order.email is not None)
        and (order.shipping_information.id is not None))) and ((order.total_price is not None) and
                                                               (order.shipping_price is not None))):

        return True

    else:
        return False


class OrderServices(object):

    @classmethod
    def initOrder(cls, data):
        response = {'orderInitialized': False, 'object': None}

        """If all the condition are respected, object will contain the order model object and if at least one condition
        is not respected, object will contain a dict with the first error."""

        if ValidateProductOrderSchema(pOrderDict=data) is True:
            pQuantity = data['product']['quantity']
            pID = data['product']['id']

            if CheckAvailability(pID=pID) is True:

                if CheckQuantity(pQuantity=pQuantity) is True:

                    order = Order.create(product=pID, product_quantity=pQuantity)
                    order.setTotalPrice()
                    order.setShippingPrice()
                    order.save()

                    response['orderInitialized'] = True
                    response['object'] = order

                else:
                    errordict = getMissingProductFieldErrorDict()
                    response['object'] = errordict

            else:
                errordict = getAvailabilityProductErrorDict()
                response['object'] = errordict

        else:

            errordict = getMissingProductFieldErrorDict()
            response['object'] = errordict

        return response

    @classmethod
    def getOrder(cls, id):

        order = Order.get_or_none(Order.id == id)

        return order

    @classmethod
    def getOrderDict(cls, id):
        order = Order.get_or_none(Order.id == id)
        return createOrderDict(orderModelObject=order)

    @classmethod
    def setOrderClientInfo(cls, clientInfoDict, orderID):
        methodOutput = {"set": False, "object": {}, "status_code": 422}

        if ValidateClientInfoSchema(cInfoDict=clientInfoDict) is True:
            o = Order.get_or_none(Order.id == orderID)
            if o is not None:
                if o.shipping_information is None:
                    sInfo = clientInfoDict['order']['shipping_information']
                    sInfoModelObject = ShippingInformation.get_or_none(ShippingInformation.address == sInfo[
                        'address'], ShippingInformation.postal_code == sInfo['postal_code'])

                    # check if adress already exist in the db
                    if sInfoModelObject is None:
                        o.shipping_information = ShippingInformation.create(country=sInfo['country'],
                                                                            address=sInfo['address'],
                                                                            postal_code=sInfo['postal_code'],
                                                                            city=sInfo['city'],
                                                                            province=sInfo['province'])
                    else:
                        o.shipping_information = sInfoModelObject

                    o.email = clientInfoDict['order']['email']
                    o.save()

                methodOutput["set"] = True
                methodOutput["object"] = createOrderDict(orderModelObject=o)
                methodOutput["status_code"] = 200

            else:
                methodOutput["object"] = getOrderNotFoundErrorDict()
                methodOutput["status_code"] = 404

        else:
            methodOutput["object"] = getMissingFieldErrorDict()

        return methodOutput

    @classmethod
    def setCreditCard(cls, cCardDict, orderId):
        methodOutput = {'set': False, "object": {}, "status_code": 422}
        o = Order.get_or_none(Order.id == orderId)

        if o is None:
            methodOutput['status_code'] = 404
            methodOutput['object'] = getOrderNotFoundErrorDict()

        elif ValidateRequiredFieldsForCCard(order=o) is False:
            methodOutput['object'] = getMissingOrderFieldErrorDict()

        elif ValidateCreditCardOrderSchema(cCardOrderDict=cCardDict) is False:
            methodOutput['object'] = getMissingCreditCardFieldErrorDict()

        elif not ((len(cCardDict['credit_card']['cvv']) == 3) and (cCardDict['credit_card']['cvv'].isdigit() is True)):
            methodOutput['object'] = getMissingCreditCardFieldErrorDict()

        elif o.paid is True:
            methodOutput['object'] = getOrderAlreadyPaidErrorDict()

        else:
            cCardDict["amount_charged"] = o.total_price + o.shipping_price
            paymentAPIResponse = requests.post(url=paymentAPIURL, json=cCardDict)
            statusCode = paymentAPIResponse.status_code
            if statusCode != 200:
                methodOutput['object'] = getPaymentApiStatusCodeError(statusCode=statusCode)

            else:
                responseDict = paymentAPIResponse.json()
                if "credit_card" in responseDict:

                    cCard = cCardDict["credit_card"]
                    ccModelObject = CreditCard.get_or_none(CreditCard.number == cCard['number'],
                                                           CreditCard.cvv == cCard['cvv'])
                    if ccModelObject is None:

                        c = CreditCard.create(name=cCard['name'], number=cCard['number'],
                                              expiration_month=cCard['expiration_month'],
                                              expiration_year=cCard['expiration_year'], cvv=cCard['cvv'])
                        o.credit_card = c
                    else:
                        o.credit_card = ccModelObject

                    t = Transaction.create(id=responseDict['transaction']['id'],
                                           success=responseDict['transaction']['success'],
                                           amount_charged=responseDict['transaction']['amount_charged'])
                    o.transaction = t
                    o.paid = True
                    o.save()

                    methodOutput['set'] = True
                    methodOutput['status_code'] = 200
                    methodOutput['object'] = createOrderDict(orderModelObject=o)

                else:
                    '''
                    On ne vérifie pas si le numéro de carte de crédit est 4242 4242 4242 4242 ou 4000 0000 0000 0002 car 
                    ça devrait être l'api distant qui le fait, donc on ne fait que transmettre le message d'erreur de l'api
                    distant au client lorsqu'il y en a un.
                    '''
                    methodOutput['object'] = getCreditCardDeclinedErrorDict(responseDict)

        return methodOutput
