# invalid parameters dicts set for invalid Product model objects instanciating
def getInvalidProductDicts():
    pDicts = []

    # invalid id
    product = {"id": "a", "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid id None
    product = {"id": None, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid name
    product = {"id": "1", "name": [1, 2, 3, 4], "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid name None
    product = {"id": "1", "name": None, "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid type
    product = {"id": "1", "name": "Brown eggs", "type": 2.5, "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid type None
    product = {"id": 1, "name": "Brown eggs", "type": None, "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid description
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": {'key1': 1, 'key2': 2},
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid description None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": None,
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid image
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": True, "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid image None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": None, "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid height type
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": "600", "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid height None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": None, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid weight type
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": "abc", "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid weight None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": None, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid price type
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": "28.1", "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid price None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": None, "rating": 5, "in_stock": True}
    pDicts.append(product)

    # invalid rating
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": ["a", "b", "c", "d", "e"],
               "in_stock": True}
    pDicts.append(product)

    # invalid rating None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": None, "in_stock": True}
    pDicts.append(product)

    # invalid in_stock
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": "True"}
    pDicts.append(product)

    # invalid in_stock None
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": None}
    pDicts.append(product)

    # missing field without default value (image)
    product = {"id": 1, "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    return pDicts


# invalid parameters dicts set for invalid CreditCar model objects instanciating
# note: we don't test if the credit card number is valid here, we only test the model attributes
# note2: the id of the CreditCard table is auto incremented.
def getInvalidCreditCardDicts():
    cCardDicts = []

    # invalid id
    cCard = {"id": "1", "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid id None
    cCard = {"id": None, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242",
             "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid name
    cCard = {"id": 1, "name": 1234, "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid name None
    cCard = {"id": 1, "name": None, "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid number
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": 4242424242424242, "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid number None
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": None, "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid expiration_year
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": "2024",
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid expiration_year None
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": None,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid cvv
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": 123, "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid cvv None
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": None, "expiration_month": 9}
    cCardDicts.append(cCard)

    # invalid expiration_month
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": "9"}
    cCardDicts.append(cCard)

    # invalid expiration_month None
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": None}
    cCardDicts.append(cCard)

    # missing field (name)
    cCard = {"id": 1, "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": None}
    cCardDicts.append(cCard)

    return cCardDicts


def getInvalidTransactionDicts():
    tDicts = []

    # invalid id
    t = {"id": 1234, "success": True, "amount_charged": 123.50}
    tDicts.append(t)

    # invalid id None
    t = {"id": None, "success": True, "amount_charged": 123.50}
    tDicts.append(t)

    # invalid success
    t = {"id": "abcde1234", "success": "True", "amount_charged": 123.50}
    tDicts.append(t)

    # invalid success None
    t = {"id": "abcde1234", "success": None, "amount_charged": 123.50}
    tDicts.append(t)

    # invalid amount_charged
    t = {"id": "abcde1234", "success": True, "amount_charged": "123.50"}
    tDicts.append(t)

    # missing field (success)
    t = {"id": "abcde1234", "amount_charged": "123.50"}
    tDicts.append(t)

    return tDicts


# note: the id of ShippingInformation is auto incremented.
def getInvalidShipInfoDicts():
    sInfoDicts = []

    # invalid id
    sInfo = {"id": "1", "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid id None
    sInfo = {"id": None, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid country
    sInfo = {"id": 1, "country": 123, "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid country None
    sInfo = {"id": 1, "country": None, "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid address
    sInfo = {"id": 1, "country": "Canada", "address": ["abc", "def"], "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid address None
    sInfo = {"id": 1, "country": "Canada", "address": None, "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid postal_code
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": 2.5,
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid postal_code None
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": None,
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid city
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": 123, "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid city None
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": 123, "province": "QC"}
    sInfoDicts.append(sInfo)

    # invalid province
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": 123, "province": 2.5}
    sInfoDicts.append(sInfo)

    # invalid province None
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": 123, "province": None}
    sInfoDicts.append(sInfo)

    # msiing field (country)
    sInfo = {"id": 1, "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": 123, "province": None}
    sInfoDicts.append(sInfo)

    return sInfoDicts


def getInvalidOrderDicts():
    oDicts = []

    # invalid id
    o = {"id": "a", "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid id None
    o = {"id": None, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid shipping information
    o = {"id": 1, "shipping_information": "1", "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid creditcard
    o = {"id": 1, "shipping_information": 1, "credit_card": "1", "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid email
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": 1,
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid total_price
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": "124.5", "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid transaction
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": 1, "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid paid
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": "False", "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid paid None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": None, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid product
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": 1, "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid product None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": None, "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid product_quantity
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": "2",
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid product_quantity None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": None,
         "shipping_price": 2.50}
    oDicts.append(o)

    # invalid shipping_price
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": "2.50"}
    oDicts.append(o)

    # missing field (product)
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1", "paid": False, "product_quantity": 2, "shipping_price": 2.50}
    oDicts.append(o)

    return oDicts


def getInvalidClientInfoDicts():
    cInfoDicts = []

    # missing order
    cInfo = {
        "email": "j.gnault@uqac.ca", "shipping_information":
            {
                "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
                "city": "Chicoutimi", "province": "QC"
            }

    }
    cInfoDicts.append(cInfo)

    # invalid email
    cInfo = {
        "order":
            {
                "email": 1, "shipping_information":
                {
                    "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
                    "city": "Chicoutimi", "province": "QC"
                }
            }
    }
    cInfoDicts.append(cInfo)

    # invalid email None
    cInfo = {
        "order":
            {
                "email": None, "shipping_information":
                {
                    "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
                    "city": "Chicoutimi", "province": "QC"
                }
            }
    }
    cInfoDicts.append(cInfo)

    # missing shipping_information
    cInfo = {
        "order":
            {
                "email": "j.gnault@uqac.ca"
            }
    }
    cInfoDicts.append(cInfo)

    # shipping_information None
    cInfo = {
        "order":
            {
                "email": "j.gnault@uqac.ca", "shipping_information": None
            }
    }
    cInfoDicts.append(cInfo)

    # invalid shipping_information (missing country)
    cInfo = {
        "order":
            {
                "email": "j.gnault@uqac.ca", "shipping_information":
                {
                    "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
                    "city": "Chicoutimi", "province": "QC"
                }
            }
    }
    cInfoDicts.append(cInfo)

    return cInfoDicts


def getInvalidProductOrderDicts():
    pOrderDict = []

    # missing product and invalid list
    pOrder = {
        "id": 1,
        "quantity": 2
    }
    pOrderDict.append(pOrder)

    # invalid id
    pOrder = {
        "product": [{
            "id": "1",
            "quantity": 2
        }]
    }
    pOrderDict.append(pOrder)

    # id None
    pOrder = {
        "product": [{
            "id": None,
            "quantity": 2
        }]
    }
    pOrderDict.append(pOrder)

    # missing id
    pOrder = {
        "product": [{
            "quantity": 2
        }]
    }
    pOrderDict.append(pOrder)

    # invalid quantity
    pOrder = {
        "product": [{
            "id": 1,
            "quantity": "2"
        }]
    }
    pOrderDict.append(pOrder)

    #  quantity None
    pOrder = {
        "product": [{
            "id": 1,
            "quantity": None
        }]
    }
    pOrderDict.append(pOrder)

    # missing quantity
    pOrder = {
        "product": [{
            "id": 1
        }]
    }
    pOrderDict.append(pOrder)

    # 2 products extra field
    pOrder = {
        "product": [
            {
                "id": 1,
                "quantity": 2
            },
            {
                "id": 2,
                "quantity": 2,
                "extra_field": "blablabla"
            }],

    }
    pOrderDict.append(pOrder)

    # extra field 2
    pOrder = {
        "product": [{
            "id": 1,
            "quantity": 2
        }],

        "extra_field": 1
    }
    pOrderDict.append(pOrder)

    return pOrderDict


def getInvalidBasicProductOrderDict():
    pOrderDicts = []

    pBasicOrder = {"id": "asd", "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 2.5, "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": True, "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": ["asd"], "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": {"asd":1}, "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": "1"}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": 2.5}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": False}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": [1]}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": {"1":1}}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={ "quantity": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={}
    pOrderDicts.append(pBasicOrder)

    pBasicOrder={"id": 1, "quantity": 1,"extra":{"extra_content":"asdasds"}}
    pOrderDicts.append(pBasicOrder)

    return pOrderDicts


def getValidProductDict():
    pDicts = []

    # normal
    product = {"id": "1", "name": "Brown eggs", "type": "dairy", "description": "Raw organic brown eggs in a basket",
               "image": "0.jpg", "height": 600, "weight": 400, "price": 28.1, "rating": 5, "in_stock": True}
    pDicts.append(product)

    return pDicts


def getValidCreditCardDicts():
    cCardDicts = []

    # explicit id
    cCard = {"id": 1, "name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    # without id (auto incremented field)
    cCard = {"name": "Jimmy Girard-Nault", "number": "4242 4242 4242 4242", "expiration_year": 2024,
             "cvv": "123", "expiration_month": 9}
    cCardDicts.append(cCard)

    return cCardDicts


def getValidShipInfoDicts():
    sInfoDicts = []

    # explicit id
    sInfo = {"id": 1, "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    # without id (auto incremented field)
    sInfo = {"country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
             "city": "Chicoutimi", "province": "QC"}
    sInfoDicts.append(sInfo)

    return sInfoDicts


def getValidTransactionDicts():
    tDicts = []

    # normal
    t = {"id": "1234", "success": True, "amount_charged": 123.50}
    tDicts.append(t)

    # normal
    t = {"id": "1234", "success": True, "amount_charged": None}
    tDicts.append(t)

    return tDicts


def getValidOrderDicts():
    oDicts = []

    # explicit id
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # without id
    o = {"shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # shipping_information None
    o = {"id": 1, "shipping_information": None, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # without shiiping_information
    o = {"id": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # credit_card None
    o = {"id": 1, "shipping_information": 1, "credit_card": None, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # credit_card missing
    o = {"id": 1, "shipping_information": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # email None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": None,
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # email missing
    o = {"id": 1, "shipping_information": 1, "credit_card": 1,
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # total_price None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": None, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # total_price missing
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "transaction": "1", "paid": False, "product": "1", "product_quantity": 2, "shipping_price": 2.50}
    oDicts.append(o)

    # transaction none
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": None, "paid": True, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # transaction missing
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # paid missing
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "product": "1", "product_quantity": 2,
         "shipping_price": 2.50}
    oDicts.append(o)

    # shipping_price None
    o = {"id": 1, "shipping_information": 1, "credit_card": 1, "email": "j.gnault@uqac.ca",
         "total_price": 124.5, "transaction": "1234", "paid": False, "product": "1", "product_quantity": 2,
         "shipping_price": None}
    oDicts.append(o)

    return oDicts


def getValidClientInfoDict():
    cInfoDicts = []

    cInfo = {
        "order":
            {
                "email": "j.gnault@uqac.ca", "shipping_information":
                {
                    "country": "Canada", "address": "201, rue Président-Kennedy", "postal_code": "G7X 3Y7",
                    "city": "Chicoutimi", "province": "QC"
                }
            }
    }
    cInfoDicts.append(cInfo)

    return cInfoDicts


def getValidProductOrderDict():
    pOrderDicts = []
    pOrder = {
        "product": [
            {
                "id": 1,
                "quantity": 2
            }
        ]
    }
    pOrderDicts.append(pOrder)

    pOrder = {
        "product": [
            {
                "id": 1,
                "quantity": 2
            },
            {
                "id": 2,
                "quantity": 1
            }
        ]
    }
    pOrderDicts.append(pOrder)

    return pOrderDicts


def getValidBasicProductOrderDict():
    bpOrderDict=[]
    bpOrder = {
        "id": 1,
        "quantity": 2
    }
    bpOrderDict.append(bpOrder)

    return bpOrderDict
