from flask import Flask, request, redirect, url_for
from api8inf349.product_table_init import InitializeProduct
from api8inf349.models import init_app, Product, Transaction, CreditCard, ShippingInformation
from api8inf349.services import OrderServices, getOrderNotFoundErrorDict
import json


def create_app():
    app = Flask(__name__)
    init_app(app)
    InitializeProduct()


    @app.route('/')
    def ProductsGET():

        prod = Product.select()
        prodsDict = {"products": []}
        for p in prod:
            prodsDict["products"].append(
                {'id': p.id, 'name': p.name, 'type': p.type, 'description': p.description, 'image': p.image,
                 "height": p.height, "weight": p.weight, "price": p.price, "rating": p.rating, "in_stock": p.in_stock})

        return app.response_class(response=json.dumps(prodsDict), status=200, mimetype='application/json')

    @app.route('/order', methods=['POST'])
    def CreateOrder():
        r = request.get_json(force=True)
        orderInitResponse = OrderServices.initOrder(r)

        if orderInitResponse['status_code'] == 200:
            id = orderInitResponse['object']
            print(type(id))
            return redirect(url_for("OrderGET", order_id=id))

        else:
            return app.response_class(response=json.dumps(orderInitResponse['object']),
                                      status=orderInitResponse["status_code"], mimetype='application/json')

    @app.route('/order/<int:order_id>', methods=['GET'])
    def OrderGET(order_id):
        response = OrderServices.getOrderDict(id=order_id)


        return app.response_class(response=json.dumps(response["object"]), status=response["status_code"],
                                  mimetype='application/json')

    @app.route('/order/<int:order_id>', methods=['PUT'])
    def AddClientInfoToOrder(order_id):
        dataDict = request.get_json(force=True)
        if "order" in dataDict:
            response = OrderServices.setOrderClientInfo(clientInfoDict=dataDict, orderID=order_id)

        else:  # elif "credit_card" in dataDict:
            response = OrderServices.setCreditCard(cCardDict=dataDict, orderId=order_id)

        return app.response_class(response=json.dumps(response['object']), status=response['status_code'],
                                  mimetype='application/json')

    return app


if __name__ == '__main__':
    create_app().run()
