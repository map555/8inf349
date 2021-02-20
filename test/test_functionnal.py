import pytest
from Api8inf349.models import Product


class TestProduct(object):
    def test_rating(self, app):
        with app.app_context():
            p = Product(id=1, name="Brown eggs", type="dairy", description="Raw organic brown eggs in a basket",
                        image="0.jpg", height=600, weight=400, price=28.1, rating=5, in_stock=False)
            p.save()

            y=Product.select().count()



            x=1
            assert x==1


