import pytest

from app.transactions import Transactions
from app.models.special import SpecialModel
from app.models.product import ProductModel

class TestTransactions(object):
    @pytest.mark.parametrize(('test_product_code', 'test_product_code_link', 'test_special_code'), (
                            ('AP1', 'AP1', 'APPL'),
                            ('CF1', 'CF1', 'BOGO')
    ))
    def test_instance_init(self, app, test_product_code, test_product_code_link, test_special_code):
        with app.app_context():
            test_product_obj =  ProductModel.find_by_product_codes([test_product_code])[0]
        
            test_list_specials_obj = [SpecialModel.find_by_special_product_code_link(test_product_code_link)]

        test_obj = Transactions(test_product_obj, test_list_specials_obj)

        assert test_obj.basket_item['product_code'] in test_product_code
        assert test_obj.specials_data_list[0]['special_code'] in test_special_code
    
    @pytest.mark.parametrize(('test_product_code', 'test_product_code_link', 'test_special_code'), (
                            ('AP1', 'AP1', 'APPL'),
                            ('CF1', 'CF1', 'BOGO')
    ))
    def test_calc_multi_special(self, app, test_product_code, test_product_code_link, test_special_code):
        with app.app_context():
            test_product_obj =  ProductModel.find_by_product_codes([test_product_code])[0]
        
            test_list_specials_obj = [SpecialModel.find_by_special_product_code_link(test_product_code_link)]

        test_obj = Transactions(test_product_obj, test_list_specials_obj)

        for test_item in test_obj.calc_multi_special():
            assert 'specials' in test_item
            assert 'special_discount' in test_item

    @pytest.mark.parametrize(('test_product_code', 'test_num_of_objs', 'product_list_expected', 'data_dict_expected'), (
                            ('AP1', 2, 2, None),
                            ('AP1', 4, 0, 4)
    ))
    def test_ap1_special_rule(self, app, test_product_code, test_num_of_objs, product_list_expected, data_dict_expected):
        with app.app_context():
            test_product_obj =  ProductModel.find_by_product_codes([test_product_code])[0]

            test_product_list, test_discount_data_dict = Transactions.ap1_special_rule(test_num_of_objs, test_product_obj)

        assert len(test_product_list) == product_list_expected
        assert test_discount_data_dict.get('num_to_apply') is data_dict_expected