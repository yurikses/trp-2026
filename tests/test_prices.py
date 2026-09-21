from prices import Price, compare_prices
from products import Category, Product
from stores import Store


def test_compare_prices_sorts_by_price():
    product = Product(1, "Телефон", Category(1, "Электроника"))
    store = Store(1, "Магазин", "https://example.com")
    prices = [Price(product, store, 200, "https://example.com/2"),
              Price(product, store, 100, "https://example.com/1")]

    assert [item.price for item in compare_prices(prices, product)] == [100, 200]
