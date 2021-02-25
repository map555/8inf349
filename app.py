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



with app.app_context():
    InitializeProduct()

if __name__ == '__main__':
    app.run()
