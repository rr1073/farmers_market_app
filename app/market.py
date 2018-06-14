from flask import (
    Blueprint, flash, redirect, render_template, url_for, session        
)

from app.models.product import ProductModel
from app.models.special import SpecialModel
from app.transactions import Transactions
from app.basket import Basket

from collections import Counter

bp = Blueprint('market', __name__)

@bp.route('/')
def index():
    items = ProductModel.get_all_items()

    cart_list = get_cart_items()

    return render_template('market/index.html', items=items, cart_list=cart_list)

@bp.route('/add-to-cart/<product_code>')
def add_to_cart(product_code):
    if session.get('cart_list') is None:
        session['cart_list'] = []
    
    session['cart_list'].append(product_code)
    flash('item added!')

    return redirect(url_for('market.index'))

def get_cart_items():
    if session.get('cart_list') is None:
        return []
    else:
        return session['cart_list']

@bp.route('/specials')
def specials():
    cart_list = get_cart_items()
    items = SpecialModel.get_all_items()

    return render_template('market/specials.html', items=items, cart_list=cart_list)

@bp.route('/emptycart')
def empty_cart():
    cart_list = get_cart_items()

    if cart_list:
        session.pop('cart_list', None)

    return redirect(url_for('market.show_cart'))

@bp.route('/show-cart')
def show_cart():
    cart_list = get_cart_items()

    if not cart_list:
        flash('Cart is empty!')
        return render_template('market/cart.html')

    basket_obj = Basket(cart_list)

    processed_items_list = basket_obj.calc_basket_total_price()

    return render_template('market/cart.html', 
                            product_data=processed_items_list, 
                            cart_list=cart_list)