from urllib.request import Request, urlopen
from other import productURL
import json
from Api8inf349.models import Product
from peewee import Model


def getRequest(url):
    r = Request(productURL)
    response = urlopen(r)
    code = response.getcode()
    if code != 200:
        print("ERROR: trying to get products from \"http://jgnault.ddns.net/shops/products/\" return http code", code)
        exit(0)
    return response


def ConvertResponseToJson(response):
    jsn = None
    try:
        jsn = json.loads(response.read())
    except Exception as exept:
        print(exept)
    return jsn


def getProducts():
    response = getRequest(url=productURL)
    jsonDict = ConvertResponseToJson(response=response)
    return jsonDict


def PopulateProduct(ProductsDict):
    try:

        for p in ProductsDict['products']:
            Product.create(id=int(p['id']), name=p['name'], type=p['type'],
                           description=p['description'], image=p['image'], height=p['height'], weight=p['weight'],
                           price=p['price'], rating=p['rating'], in_stock=p['in_stock'])

    except Exception as exept:
        print(exept)
        exit(0)


def CheckExistance_Test(app, jsonProduct):
    with app.app_context():
        count = None

        try:
            id = int(jsonProduct['id'])
            count = Product.select().where(Product.id == id).count()
            print()
        # if an error happens like failed to connect to bd
        except Exception as exept:
            print(exept)  # because it's an homework, we print each error
            exit(0)

        else:

            if count == 1:
                return True

            elif count == 0:
                return False


def CheckExistance(jsonProduct):
    count = None

    try:
        id = int(jsonProduct['id'])
        count = Product.select().where(Product.id == id).count()
        print()
    # if an error happens like failed to connect to bd
    except Exception as exept:
        print(exept)  # because it's an homework, we print each error
        exit(0)

    else:

        if count == 1:
            return True

        elif count == 0:
            return False


# we dont test this one because CheckExistance and bd insert are already tested.
def UpdateProduct(ProductsDict):
    for p in ProductsDict['products']:
        if not CheckExistance(p):
            x = Product.select().count()
            Product.create(id=x + 1, name=p['name'], type=p['type'],
                           description=p['description'], image=p['image'], height=p['height'], weight=p['weight'],
                           price=p['price'], rating=p['rating'], in_stock=p['in_stock'])


def InitializeProduct():
    products = getProducts()
    UpdateProduct(ProductsDict=products)  # check if update
