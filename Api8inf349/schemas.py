from schema import Schema, And, Optional, Or

# for insert validation
# note: the schema doesn't test the integrity constraint because the database will check it.
ProductSchema = Schema({
    'id': And(str, lambda ID: ID.isnumeric()),
    'name': str,
    'type': str,
    'description': str,
    'image': str,
    'height': int,
    'weight': int,
    'price': float,
    'rating': int,
    'in_stock': bool
})

ProductListSchema = Schema({
    'products': [ProductSchema]
})

ProductOrderBasicSchema = Schema({
    "id": int,
    "quantity": int
})

ProductOrderSchema = Schema({
    "product": [ProductOrderBasicSchema]
})

ShippingInformationSchema = Schema({
    Optional('id'): int,  # auto incremented id
    'country': str,
    'address': str,
    'postal_code': str,
    'city': str,
    'province': str
})

ClientInfoSchema = Schema({
    'order': {
        "email": str,
        "shipping_information": ShippingInformationSchema
    }
})

CreditCardSchema = Schema({
    Optional('id'): int,  # auto incremented id
    'name': str,
    'number': str,
    'expiration_month': int,
    'expiration_year': int,
    'cvv': str
})

CreditCardOrderSchema = Schema({
    "credit_card": CreditCardSchema
})

TransactionSchema = Schema({
    'id': str,
    'success': bool,
    'amount_charged': Or(float, None)
})

OrderSchema = Schema({
    Optional('id'): int,  # auto incremented id
    Optional('shipping_information'): Or(int, None),  # this field allows null and has a default value
    Optional('credit_card'): Or(int, None),
    Optional('email'): Or(str, None),
    Optional('total_price'): Or(float, None),
    Optional('transaction'): Or(str, None),
    Optional('paid'): bool,  # this field has default value
    'product': str,
    'product_quantity': int,
    Optional('shipping_price'): Or(float, None)
})
