from model import Product


class TestProduct(object):

    #normal case
    def test_init(self):
        p=Product(id=1, name="Brown eggs", type="dairy", description="Raw organic brown eggs in a basket",
                  image="0.jpg", height=600, weight=400, price=28.1,rating=4, in_stock=True)

        assert p.id==1
        assert p.name=="Brown eggs"
        assert p.type=="dairy"
        assert p.description=="Raw organic brown eggs in a basket"
        assert p.image=="0.jpg"
        assert p.height==600
        assert p.weight==400
        assert p.price ==28.1
        assert p.rating==4
        assert p.in_stock==True


