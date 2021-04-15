from flask import Flask, request, redirect, url_for
from api8inf349.product_table_init import InitializeProduct
from api8inf349.models import init_app, Product, Transaction, CreditCard, ShippingInformation
from api8inf349.services import OrderServices, getOrderNotFoundErrorDict
import json
from api8inf349.db import getRedis
from api8inf349.models import getDB
from rq.job import Job
from rq import Queue, Worker
# from rq_win import WindowsWorker as Worker


def create_app():
    app = Flask(__name__)
    init_app(app)
    

    queue = Queue(connection=getRedis())

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

        job = queue.fetch_job(str(order_id))

        if (job is not None) and not job.is_finished:
            return '', 202

        response = OrderServices.getOrderDict(id=order_id)

        return app.response_class(response=json.dumps(response["object"]), status=response["status_code"],
                                  mimetype='application/json')

    @app.route('/order/<int:order_id>', methods=['PUT'])
    def AddClientInfoToOrder(order_id):
        dataDict = request.get_json(force=True)

        job = queue.fetch_job(str(order_id))
        if job is not None:
            if not job.is_finished:
                return '', 409

        if "order" in dataDict:
            response = OrderServices.setOrderClientInfo(clientInfoDict=dataDict, orderID=order_id)

        else:  # elif "credit_card" in dataDict:
            job = queue.enqueue(OrderServices.setCreditCard, dataDict, order_id, job_id=str(order_id))
            return redirect(url_for('verifyPaymentJob', job_id=job.id))

        return app.response_class(response=json.dumps(response['object']), status=response['status_code'],
                                  mimetype='application/json')

    @app.route("/job/<string:job_id>")
    def verifyPaymentJob(job_id):
        job = queue.fetch_job(job_id)
        if not job.is_finished:
            return '', 202

        return job.result

    @app.cli.command("worker")
    def rq_worker():
        worker = Worker([queue], connection=getRedis())
        worker.work()

    return app


if __name__ == '__main__':
    create_app().run()
    InitializeProduct()
