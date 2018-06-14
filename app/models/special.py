from app.extensions import dbalch

class SpecialModel(dbalch.Model):
    __tablename__ = 'specials'

    id = dbalch.Column(dbalch.Integer, primary_key=True)
    special_code = dbalch.Column(dbalch.String(80), nullable=False)
    special_description = dbalch.Column(dbalch.String(80), nullable=False)
    special_limit = dbalch.Column(dbalch.Integer)
    special_discount = dbalch.Column(dbalch.Numeric(15, 2), nullable=False)
    special_product_code_link = dbalch.Column(dbalch.String(80), nullable=False)
    special_discount_rate = dbalch.Column(dbalch.Numeric(15, 2), nullable=False)

    def __init__(self, special_code, special_description, special_limit,
                 special_discount, special_product_code_link, special_discount_rate):
        # self.id = _id
        self.special_code = special_code
        self.special_description = special_description
        self.special_limit = special_limit
        self.special_discount = special_discount
        self.special_product_code_link = special_product_code_link
        self.special_discount_rate = special_discount_rate

    def __repr__(self):
        return (f'SpecialModel special_code: {self.special_code}, '
                f'special_description: {self.special_description}, ' 
                f'special_limit: {self.special_limit}, specail_discount: {self.special_discount}, '
                f'special_product_code_link: {self.special_product_code_link}, '
                f'special_discount_rate: {self.special_discount_rate}')

    def obj_to_dict(self):
        return {'special_code': self.special_code,
                'special_description': self.special_description, 
                'special_limit': self.special_limit, 
                'special_discount': self.special_discount, 
                'special_product_code_link': self.special_product_code_link,
                'special_discount_rate': self.special_discount_rate}

    @classmethod
    def multi_find_by_special_product_code_link(cls, codes):
        results = cls.query.filter(cls.special_product_code_link.in_(codes)).all()
        return [item.obj_to_dict() for item in results]

    @classmethod
    def find_by_special_product_code_link(cls, code):
        result = cls.query.filter_by(special_product_code_link=code).first()
        return result.obj_to_dict()

    @classmethod
    def get_all_items(cls):
        results = cls.query.all()
        return [item.obj_to_dict() for item in results]