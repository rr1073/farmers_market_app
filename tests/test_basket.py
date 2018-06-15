import pytest

from app.basket import Basket
from app.models.special import SpecialModel
from app.models.product import ProductModel

class TestBasket(object):
    def test_instance_init(self, app):
        test_item_list = ['AP1', 'CF1', 'OM1']
        test_obj = Basket(test_item_list)

        assert 3 == len(test_obj.basket_item_codes)
        assert 'AP1' in test_obj.basket_item_codes


    @pytest.mark.parametrize(('test_product_list', 'test_total_price'), (
                            (['AP1', 'AP1', 'AP1'],'$13.50'),
    ))
    def test_calc_basket_total_price(self, app, test_product_list, test_total_price):
        test_item_list = test_product_list
        test_obj = Basket(test_item_list)
        with app.app_context():
            result = test_obj.calc_basket_total_price()

        assert result[-1]['product_price'] == test_total_price

    @pytest.mark.parametrize(('test_product_list', 'basket_length'), (
                            (['AP1', 'AP1', 'AP1'], 3),
    ))
    def test_calc_num_of_items(self, app, test_product_list, basket_length):
        test_obj = Basket(test_product_list)

        assert basket_length == test_obj.calc_num_of_items()

    @pytest.mark.parametrize(('test_product_list', 'num_of_unique_basket_items'), (
                            (['AP1', 'AP1', 'AP1'], 1),
                            (['CF1', 'OM1', 'MK1'], 3)
    ))
    def test_calc_unique_item_types_in_basket(self, app, test_product_list, num_of_unique_basket_items):
        test_obj = Basket(test_product_list)

        assert num_of_unique_basket_items == len(test_obj.calc_unique_item_types_in_basket())

    def test_get_item_objs_by_code(self, app):
        test_item_list = ['AP1', 'CF1', 'OM1']
        test_obj = Basket(test_item_list)

        with app.app_context():
            result = test_obj.get_item_objs_by_code()

        assert 'AP1' in result
        assert 'Coffee' in result['CF1']['product_name']
        assert 'Oatmeal' in result['OM1']['product_name']

    @pytest.mark.parametrize(('test_product_list', 'num_of_reccuring_basket_items', 'product_code'), (
                            (['AP1', 'AP1', 'AP1'], 3, 'AP1'),
                            (['CF1', 'OM1', 'MK1'], 1, 'CF1')
    ))
    def test_calc_item_occurrences(self, app, test_product_list, num_of_reccuring_basket_items, product_code):
        test_obj = Basket(test_product_list)

        result = test_obj.calc_item_occurrences()

        assert result[product_code] == num_of_reccuring_basket_items
    @pytest.mark.parametrize(('test_product_list', 'test_product_code', 'option'), (
                            (['AP1', 'AP1'], 'AP1', None),
                            (['CF1', 'CF1'], 'CF1', 'CF1')
    ))
    def test_calc_basket_items(self, app, test_product_list, test_product_code, option):
        test_item_list = test_product_list
        test_obj = Basket(test_item_list)

        test_list_specials_obj = None
        test_product_obj = None

        with app.app_context():
            test_product_obj_list =  ProductModel.find_by_product_codes([test_product_code])
            

            if option:
                test_list_specials_obj = [SpecialModel.find_by_special_product_code_link(option)]
                test_product_obj = test_product_obj_list[0]


            test_obj.calc_basket_items(test_product_obj_list, test_product_obj, test_list_specials_obj)

            for item in test_obj.processed_basket_list:
                if not option:
                    assert 'specials' not in item
                else:
                    assert 'product_price' in item
    
    @pytest.mark.parametrize(('test_product_occurences', 'test_product_code', 'specials_type'), (
                            ({'AP1': 3}, 'AP1', 'APPL'),
    ))
    def test__check_for_specials_and_discounts(self, app, test_product_occurences, test_product_code, specials_type):
        test_item_list = [test_product_code] * test_product_occurences[test_product_code]
        test_obj = Basket(test_item_list)
        test_product_obj = {}.setdefault(test_product_code, {})

        with app.app_context():
            test_product_obj[test_product_code] =  ProductModel.find_by_product_codes([test_product_code])[0]

            test_obj._check_for_specials_and_discounts(test_product_occurences, test_product_obj)

        assert test_obj.processed_basket_list[0]['specials'][0]['special_code'] in specials_type
            