from Api8inf349.models import Product, Order, Transaction, CreditCard, ShippingInformation
from peewee import DoesNotExist

def getMissingProductFieldErrorDict(dict):
    dict['errors']['product']['code'] = "missing-fields"
    dict['errors']['product']['name'] = "The creation of an order requires a single product. " \
                                        "The product dict must have the following form: { 'product': " \
                                        "{ 'id': id, 'quantity': quantity } }. Quantity must be an integer > 0."

    return dict


def getAvailabilityProductErrorDict(dict):
    dict['errors']['product']['code'] = "out-of-inventory"
    dict['errors']['product']['name'] = "The product you asked for is not in the inventory for now."

    return dict


def CheckIfOneProduct(data):
    if len(data["product"]) == 2 and ("id" in data["product"] and "quantity" in data["product"]):
        if type(data['product']['id']) == int:
            p = Product.get_or_none(Product.id == data["product"]['id'])
            if p is not None:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def CheckQuantity(data):
    if type(data["product"]["quantity"]) == int:
        if data["product"]["quantity"] > 0:
            return True
        else:
            return False
    else:
        return False


def CheckAvailability(data):
    p = Product.get_by_id(data["product"]["id"])
    if p.in_stock is True:
        return True
    else:
        return False



class OrderServices(object):

    @classmethod
    def initOrder(cls, data):
        response = {'orderInitialized': False, 'object': None}
        errordict = {'errors': {'product': {"code": "", "name": ""}}}
        oneProduct = CheckIfOneProduct(data=data)

        """If all the condition are respected, object will contain the order model object and if at least one condition
        is not respected, object will contain a dict with the first error."""

        if oneProduct is True:
            quantityOk = CheckQuantity(data=data)

            if quantityOk is True:
                available = CheckAvailability(data=data)

                if available is True:
                    response['orderInitialized'] = True
                    response['object'] = Order.create(product=data["product"]["id"],
                                                      product_quantity=data["product"]["quantity"])

                    return response

                else:
                    errordict = getAvailabilityProductErrorDict(errordict)
                    response['object'] = errordict
                    return response

            else:
                errordict = getMissingProductFieldErrorDict(errordict)
                response['object'] = errordict
                return response

        else:

            errordict = getMissingProductFieldErrorDict(errordict)
            response['object'] = errordict
            return response

