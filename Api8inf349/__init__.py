from flask import Flask, request, redirect, url_for, abort
from Api8inf349.models import init_app, Product, Transaction, CreditCard, ShippingInformation


def create_app(initial_config=None):
    app = Flask("Api8inf439")
    init_app(app)
    return app

