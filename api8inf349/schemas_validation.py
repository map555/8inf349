from api8inf349.schemas import *

"""
ALL THE FUNCTIONS IN THIS FILE WILL RETURN TRUE OR FALSE DEPENDING
IF THE DICTIONNARY PASSED TO THE FUNCTION IS CONFORM TO THE SCHEMA.
"""


def ValidateProductSchema(pDict):
    return ProductSchema.is_valid(pDict)


def ValidateProductListSchema(pListDict):
    return ProductListSchema.is_valid(pListDict)


def ValidateBasicProductOrderSchema(pBasicOrderDict):
    return ProductOrderBasicSchema.is_valid(pBasicOrderDict)


def ValidateProductOrderSchema(pOrderDict):
    return ProductOrderSchema.is_valid(pOrderDict)


def ValidateTransactionSchema(tDict):
    return TransactionSchema.is_valid(tDict)


def ValidateShippingInfoSchema(sInfoDict):
    return ShippingInformationSchema.is_valid(sInfoDict)


def ValidateOrderSchema(oDict):
    return OrderSchema.is_valid(oDict)


def ValidateCreditCardSchema(cCardDict):
    return CreditCardSchema.is_valid(cCardDict)


def ValidateCreditCardOrderSchema(cCardOrderDict):
    return CreditCardOrderSchema.is_valid(cCardOrderDict)


def ValidateClientInfoSchema(cInfoDict):
    return ClientInfoSchema.is_valid(cInfoDict)
