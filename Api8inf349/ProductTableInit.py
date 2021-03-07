from urllib.request import Request, urlopen
from Api8inf349.url import productURL
import json
from Api8inf349.schemasValidation import ValidateProductListSchema
from Api8inf349.models import Product


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


def CheckExistance_Test(app, jsonProduct):
    with app.app_context():

        id = int(jsonProduct['id'])
        query = Product.select().where(Product.id == id)

        if query.exists():
            return True

        else:
            return False


def CheckExistance(jsonProduct):
    id = int(jsonProduct['id'])
    query = Product.select().where(Product.id == id)

    if query.exists():
        return True

    else:
        return False


# we dont test this one because CheckExistance and bd insert are already tested.
def UpdateProduct(ProductsDict):
    if ValidateProductListSchema(ProductsDict) is True:
        for p in ProductsDict['products']:
            if not CheckExistance(p):
                Product.create(name=p['name'], type=p['type'], description=p['description'], image=p['image'],
                               height=p['height'], weight=p['weight'], price=p['price'], rating=p['rating'],
                               in_stock=p['in_stock'])
    else:
        print("ERROR: INVALID PRODUCT!\nTHE PROGRAM WILL NOW EXIT.")
        exit(0)


def InitializeProduct():
    products = getProducts()
    UpdateProduct(ProductsDict=products)  # check if update
