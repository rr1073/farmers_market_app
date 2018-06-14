from collections import Counter

from app.models.product import ProductModel
from app.models.special import SpecialModel
from app.transactions import Transactions

class Basket(object):
    """ class Basket used for dealing with basket items such as delegating transactions and specials/discounts"""

    def __init__(self, basket_item_codes):
        """
        initialize the Basket object with a list of product item codes

        :param basket_item_codes: list of str that represent product item codes
        
        """

        self.basket_item_codes = basket_item_codes

        self.running_total = 0.0
        self.processed_basket_list = []

    def calc_basket_total_price(self):
        """
        driver for Basket operations performed for each item within it
        
        :return: list of dict objs that contain processed product data including
                 the total price of the current basket (last element)
        """

        product_occurrences = self.calc_item_occurrences()
        item_objs = self.get_item_objs_by_code()

        self._check_for_specials_and_discounts(product_occurrences, item_objs)

        for basket_item in self.processed_basket_list:
            self.running_total += float(basket_item['product_price'])
            if 'specials' in basket_item:
                for special in basket_item['specials']:
                    self.running_total -= float(special['special_discount'])

        self.processed_basket_list.append({'product_price': '$' + '{0:.2f}'.format(self.running_total)})

        return self.processed_basket_list

    def calc_num_of_items(self):
        return len(self.basket_item_codes)

    def calc_unique_item_types_in_basket(self):
        return set(self.basket_item_codes)

    def get_item_objs_by_code(self):
        """
        get the Product data models represented in the current basket instance

        :return: dict obj representing the Product(s) data model
        """

        item_data_dict = ProductModel.find_by_product_codes(self.calc_unique_item_types_in_basket())

        return {row['product_code']: row for row in item_data_dict}

    def calc_item_occurrences(self):
        return Counter(self.basket_item_codes)

    def calc_basket_items(self, reg_transaction_items, special_transaction_item=None, specials_data_list=None):
        """
        process batch of similar product items and calculate discount(s), if any 

        :param reg_transaction_items: list of product obj items that will be processed without any specials applied
        :param special_transaction_item: (Default: None) Product obj item that will have discount(s)/special applied to it
        :param specials_data_list: (Default: None) list of special discount objs to apply to product items
        
        :return: None
        """

        for item in reg_transaction_items:
            self.processed_basket_list.append({'product_code': item['product_code'],
                                               'product_price':item['product_price']})

        if special_transaction_item and specials_data_list:
            transaction_obj = Transactions(special_transaction_item, 
                                                specials_data_list)

            for item in transaction_obj.calc_multi_special():
                self.processed_basket_list.append(item)

    def _check_for_specials_and_discounts(self, product_occurrences, product_objects):
        """
        Examines items(products) in basket, then depending on criterias set
        will pass objects to the Transactions and calculate discount price(s)

        :param product_occurences: dict type obj that hold the count of each item by product code
        :param product_objects: dict type obj that represent the current basket item(s) from the Product data model

        :return: None
        """
        
        discount_data_dict = {}

        if 'AP1' in product_occurrences:
            if 'OM1' in product_occurrences:
                discount_data_dict['OM1'] = SpecialModel.find_by_special_product_code_link('OM1')

                num_of_special_transactions = min(product_occurrences['OM1'], product_occurrences['AP1'])
                discount_data_dict['OM1'].update({'num_to_apply': num_of_special_transactions})

                ap1_product_list, discount_data_dict['AP1'] = Transactions.ap1_special_rule(product_occurrences['AP1'], 
                                                                                            product_objects['AP1'])

                discount_data_list = [discount_data_dict[key] for key in discount_data_dict]

                product_list = [product_objects['OM1']]*product_occurrences['OM1']

                self.calc_basket_items((product_list+ap1_product_list), product_objects['AP1'], discount_data_list)
            else:
                product_list, discount_data_dict['AP1'] = Transactions.ap1_special_rule(product_occurrences['AP1'], product_objects['AP1'])
                discount_data_list = [discount_data_dict['AP1']]

                self.calc_basket_items(product_list, product_objects['AP1'], discount_data_list)

        elif 'OM1' in product_occurrences:
            product_list = [product_objects['OM1']]*product_occurrences['OM1']

            self.calc_basket_items(product_list)

        if 'CF1' in product_occurrences:
            if product_occurrences['CF1'] >= 2:
                discount_data_dict['CF1'] = SpecialModel.find_by_special_product_code_link('CF1')

                num_of_special_transactions = (product_occurrences['CF1'] // 2)
                num_of_reg_items = product_occurrences['CF1'] - num_of_special_transactions

                discount_data_dict['CF1'].update({'num_to_apply': num_of_special_transactions})

                discount_data_list = [discount_data_dict['CF1']]

                product_list = [product_objects['CF1']]*num_of_reg_items

                self.calc_basket_items(product_list, product_objects['CF1'], discount_data_list)
            else:
                product_list = [product_objects['CF1']]*product_occurrences['CF1']

                self.calc_basket_items(product_list)

        if 'CH1' in product_occurrences and 'MK1' in product_occurrences:
            discount_data_dict['MK1'] = SpecialModel.find_by_special_product_code_link('CH1')

            num_of_special_transactions = discount_data_dict['MK1']['special_limit']
            num_of_reg_items = product_occurrences['MK1'] - num_of_special_transactions

            discount_data_dict['MK1'].update({'num_to_apply': num_of_special_transactions})

            discount_data_list = [discount_data_dict['MK1']]

            product_list = [product_objects['MK1']]*num_of_reg_items

            ch1_product_list = [product_objects['CH1']]*product_occurrences['CH1']

            self.calc_basket_items((product_list+ch1_product_list), product_objects['MK1'], discount_data_list)

        elif ('CH1' in product_occurrences or 'MK1' in product_occurrences):
            if 'MK1' in product_occurrences:
                product_list = [product_objects['MK1']]*product_occurrences['MK1']
            if 'CH1' in product_occurrences:
                product_list = [product_objects['CH1']]*product_occurrences['CH1']

            self.calc_basket_items(product_list)