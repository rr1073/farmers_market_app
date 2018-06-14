from app.extensions import dbalch

class ProductModel(dbalch.Model):
    __tablename__ = 'products'

    id = dbalch.Column(dbalch.Integer, primary_key=True)
    product_code = dbalch.Column(dbalch.String(80), nullable=False)
    product_name = dbalch.Column(dbalch.String(80), nullable=False)
    product_price = dbalch.Column(dbalch.Numeric(15, 2), nullable=False)

    def __init__(self, product_code, product_name, product_price):
        # self.id = _id
        self.product_code = product_code
        self.product_name = product_name
        self.product_price = product_price

    def __repr__(self):
        return (f'ProductModel product_code: {self.product_code}, product_name: {self.product_name}, ' 
                f'product_price: {self.product_price}')

    def obj_to_dict(self):
        return {'product_code': self.product_code,
                'product_name': self.product_name,
                'product_price': self.product_price}

    @classmethod
    def find_by_product_codes(cls, codes):
        results = cls.query.filter(cls.product_code.in_(codes)).all()
        return [item.obj_to_dict() for item in results]

    @classmethod
    def get_all_items(cls):
        results = cls.query.all()
        return [item.obj_to_dict() for item in results]