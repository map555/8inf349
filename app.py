from flask import Flask, request, redirect, url_for, abort
from Api8inf349.ProductTableInit import InitializeProduct
from Api8inf349.models import Product, Order, ShippingInformation, Transaction, CreditCard
from Api8inf349.services import OrderServices
from flask import json

app = Flask(__name__)


@app.route('/hw')
def hello_world():
    return 'Hello World!'


# TODO: implement the test(s)
@app.route('/')
def ProductsGET():
    prod = Product.select()
    prodsDict = {"products": []}
    for p in prod:
        prodsDict["products"].append(
            {'id': p.id, 'name': p.name, 'type': p.type, 'description': p.description, 'image': p.image,
             "height": p.height, "weight": p.weight, "price": p.price, "rating": p.rating, "in_stock": p.in_stock})

    return app.response_class(response=json.dumps(prodsDict),status=200,mimetype='application/json')


# TODO: implement the test(s)
@app.route('/order', methods=['POST'])
def CreateOrder():
    r = request.get_json(force=True)
    orderInitResponse = OrderServices.initOrder(r)


    if orderInitResponse['orderInitialized'] is True:
        order = orderInitResponse['object']
        return redirect(url_for("OrderGET", order_id=order.id))

    else:
        return app.response_class(response=json.dumps(orderInitResponse['object']), status=422,
                                  mimetype='application/json')




@app.route('/order/<int:order_id>', methods=['GET'])
def OrderGET(order_id):
    orderDict = OrderServices.getOrderDict(id=order_id)

    return app.response_class(response=json.dumps(orderDict),status=200,mimetype='application/json')


with app.app_context():
    InitializeProduct()

if __name__ == '__main__':
    app.run()
