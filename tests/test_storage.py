from pathlib import Path

from storage import DataRepository, load_data, save_data


def test_load_data_reads_json_files():
    data = load_data(Path(__file__).parents[1] / "data")

    assert len(data["products"]) == 3
    assert len(data["prices"]) == 7


def test_repository_supports_crud_for_all_entities(tmp_path):
    repository = DataRepository()
    category = repository.create_category("Книги")
    product = repository.create_product("Python", category.id)
    store = repository.create_store("Магазин", "https://example.com")
    price = repository.create_price(product.id, store.id, 100, "https://example.com/python")
    user = repository.create_user("Иван", "ivan@example.com")
    user.add_favorite(product)

    assert repository.get_category(category.id) is category
    assert repository.get_product(product.id) is product
    assert repository.get_store(store.id) is store
    assert repository.get_prices(product.id) == [price]
    assert repository.get_user(user.id) is user

    repository.update_category(category.id, "Литература")
    repository.update_product(product.id, name="Python 3")
    repository.update_store(store.id, name="Новый магазин")
    repository.update_price(price, price=120)
    repository.update_user(user.id, name="Петр")

    assert str(product) == "Python 3"
    assert str(store) == "Новый магазин"
    assert price.price == 120
    assert str(user) == "Петр <ivan@example.com>"

    repository.delete_product(product.id)
    repository.delete_store(store.id)
    repository.delete_user(user.id)
    repository.delete_category(category.id)
    assert repository.prices == []
    assert repository.users == {}


def test_repository_saves_and_loads_related_objects(tmp_path):
    source = load_data(Path(__file__).parents[1] / "data")
    repository = DataRepository(**source)
    repository.save(tmp_path)

    loaded = load_data(tmp_path)

    assert loaded["products"][1].category is loaded["categories"][1]
    assert loaded["prices"][0].product is loaded["products"][1]
    assert loaded["prices"][0].store is loaded["stores"][1]
    assert loaded["users"][1].favorites == []


def test_save_data_keeps_public_storage_function(tmp_path):
    data = load_data(Path(__file__).parents[1] / "data")
    save_data(tmp_path, data)

    assert len(load_data(tmp_path)["users"]) == 1
