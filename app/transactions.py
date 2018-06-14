
from app.models.special import SpecialModel

class Transactions(object):
    """ handles all manner of special transactions in Basket items """

    def __init__(self, basket_item, specials_data_list):
        """ initialize """
        self.basket_item = basket_item
        self.specials_data_list = specials_data_list

        self.processed_basket_item_list = []

    def calc_multi_special(self):
        for special_type in self.specials_data_list:
            for num in range(special_type.get('num_to_apply', 0)):
                discounted_amount = self.basket_item['product_price'] - (self.basket_item['product_price'] *
                                                                (1 - special_type['special_discount_rate']))

                try:
                    self.processed_basket_item_list[num]['specials'].append({'special_code': special_type['special_code'],
                                                                             'special_discount': '{0:.2f}'.format(discounted_amount)})
                except IndexError:
                    self.processed_basket_item_list.append({'product_code': self.basket_item['product_code'],
                                                            'product_price': self.basket_item['product_price'],
                                                            'specials': [{'special_code': special_type['special_code'],
                                                                          'special_discount': '{0:.2f}'.format(discounted_amount)}]})

        for item in self.processed_basket_item_list:
            yield item

    @staticmethod
    def ap1_special_rule(num_of_ap1_items, ap1_obj):
        discount_data_dict = {}
        product_list = []

        if num_of_ap1_items >= 3:
            discount_data_dict = SpecialModel.find_by_special_product_code_link(ap1_obj['product_code'])

            num_of_special_transactions = num_of_ap1_items
            discount_data_dict.update({'num_to_apply': num_of_special_transactions})
        else:
            product_list = [ap1_obj]*num_of_ap1_items

        return product_list, discount_data_dict
