from products import Category, Product, search_products


def test_search_products_is_case_insensitive():
    category = Category(1, "Электроника")
    products = [Product(1, "iPhone 15", category), Product(2, "Чайник", category)]

    assert search_products(products, "IPHONE") == [products[0]]
