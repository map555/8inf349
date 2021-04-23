from urllib.request import Request, urlopen
from api8inf349.url import productURL
import json
from api8inf349.schemas_validation import ValidateProductListSchema
from api8inf349.models import Product


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
    # fix the problem with the null char for product id 45
    jsn['products'][44][
        'description'] = "Healthy breakfast set. rice cereal or porridge with fresh strawberry, apricots," \
                         "almond and honey over white rustic wood backdrop, top view."

    return jsn


def getProducts():
    response = getRequest(url=productURL)
    jsonDict = ConvertResponseToJson(response=response)
    return jsonDict


def CheckExistance(jsonProduct):
    id = int(jsonProduct['id'])

    try:
        query = Product.get_or_none(Product.id == id)
        if query is not None:
            return True
        else:
            return False
    except:
        return False


# we dont test this one because CheckExistance and bd insert are already tested.
def UpdateProduct(ProductsDict):
    if ValidateProductListSchema(ProductsDict) is False:
        print("ERROR: INVALID PRODUCT!\nTHE PROGRAM WILL NOW EXIT.")
        exit(0)
    try:
        for p in ProductsDict['products']:
            checkExist = CheckExistance(p)
            if checkExist is not True:
                Product.create(name=p['name'], type=p['type'], description=p['description'], image=p['image'],
                               height=p['height'], weight=p['weight'], price=p['price'], rating=p['rating'],
                               in_stock=p['in_stock'])
    except:
        pass


def InitializeProduct():
    products = getProducts()
    UpdateProduct(ProductsDict=products)  # check if update
