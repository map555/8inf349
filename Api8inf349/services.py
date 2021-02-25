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


    @classmethod
    def getOrder(cls, id):

        order = Order.get_or_none(Order.id == id)

        return order

    @classmethod
    def getOrderDict(cls, id):
        order = Order.get_or_none(Order.id == id)

        jsonOrder = {'id': order.id, 'shipping_information': {}, 'credit_card': {}, 'email': order.email,
                     'total_price': order.total_price, 'transaction': {}, 'paid': order.paid, 'product':
                         {'product_id': order.product.id, 'product_quantity': order.product_quantity}, 'shipping_price':
                         order.shipping_price}

        if order.shipping_information is not None:
            jsonOrder['shipping_information'] = {'id': order.shipping_information.id, 'country':
                order.shipping_information.country, 'address': order.shipping_information.adress, 'postal_code':
                                                     order.shipping_information.postal_code,
                                                 'city': order.shipping_information.city, 'province':
                                                     order.shipping_information.province}

        if order.credit_card is not None:
            jsonOrder['credit_card'] = {'id': order.credit_card.id, 'name': order.credit_card.name, 'number':
                order.credit_card.number, 'expiration_month': order.credit_card.expiration_month, 'expiration_year':
                                            order.credit_card.expiration_year, 'cvv': order.credit_card.cvv}

        if order.transaction is not None:
            jsonOrder['transaction'] = {'id': order.transaction.id, 'success': order.transaction.success,
                                        'amount_charged':
                                            order.transaction.amount_charged}

        return jsonOrder
