from stores import Store


def test_store_keeps_name_and_url():
    store = Store(1, "DNS", "https://dns-shop.ru")

    assert (store.name, store.url) == ("DNS", "https://dns-shop.ru")
