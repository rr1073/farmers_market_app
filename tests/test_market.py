import pytest

from app.db import get_db

def test_index(client):
    response = client.get('/')
    assert b"see products" in response.data
    assert b"see specials" in response.data
    assert b"Show cart" in response.data

    assert b"Market Products" in response.data
    assert b"Add to cart" in response.data
    assert b"Chai" in response.data
    assert b"Apples" in response.data
    assert b"Milk" in response.data
    assert b"Coffee" in response.data
    assert b"Oatmeal" in response.data

def test_market(client):
    response = client.get('/market/')
    assert b"see products" in response.data
    assert b"see specials" in response.data
    assert b"Show cart" in response.data

def test_1(client):
    client.get('/market/add-to-cart/CH1')
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/MK1')

    response = client.get('/market/')
    assert b"Show cart (5)" in response.data
    response = client.get('/market/show-cart')
    assert b"$16.61" in response.data

def test_2(client):
    # Testing: CH1, AP1, CF1, MK1
    client.get('/market/add-to-cart/CH1')
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/CF1')
    client.get('/market/add-to-cart/MK1')

    response = client.get('/market/')
    assert b"Show cart (4)" in response.data
    response = client.get('/market/show-cart')
    assert b"$20.34" in response.data

def test_3(client):
    # Testing: MK1, AP1
    # Total price expected: $10.75
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/MK1')

    response = client.get('/market/')
    assert b"Show cart (2)" in response.data
    response = client.get('/market/show-cart')
    assert b"$10.75" in response.data

def test_4(client):
    # Testing: CF1, CF1
    # Total price expected: $11.23
    client.get('/market/add-to-cart/CF1')
    client.get('/market/add-to-cart/CF1')

    response = client.get('/market/')
    assert b"Show cart (2)" in response.data
    response = client.get('/market/show-cart')
    assert b"$11.23" in response.data

def test_5(client):
    # Testing: AP1, AP1, CH1, AP1
    # Total price expected: $16.61
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/AP1')
    client.get('/market/add-to-cart/CH1')
    client.get('/market/add-to-cart/AP1')

    response = client.get('/market/')
    assert b"Show cart (4)" in response.data
    response = client.get('/market/show-cart')
    assert b"$16.61" in response.data