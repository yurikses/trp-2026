import json
from datetime import datetime
from pathlib import Path
from typing import Any

from prices import Price
from products import Category, Product
from stores import Store
from users import User


class DataRepository:
    """Хранилище объектов с CRUD-операциями и JSON-сериализацией."""

    def __init__(self, categories: dict[int, Category] | None = None,
                 products: dict[int, Product] | None = None,
                 stores: dict[int, Store] | None = None,
                 prices: list[Price] | None = None,
                 users: dict[int, User] | None = None) -> None:
        self.categories = categories or {}
        self.products = products or {}
        self.stores = stores or {}
        self.prices = prices or []
        self.users = users or {}

    @staticmethod
    def _next_id(items: dict[int, Any]) -> int:
        return max(items, default=0) + 1

    def create_category(self, name: str, category_id: int | None = None) -> Category:
        new_id = category_id or self._next_id(self.categories)
        category = Category(new_id, name)
        self.categories[new_id] = category
        return category

    def get_category(self, category_id: int) -> Category | None:
        return self.categories.get(category_id)

    def update_category(self, category_id: int, name: str) -> Category:
        category = self.categories[category_id]
        category.name = name
        return category

    def delete_category(self, category_id: int) -> None:
        del self.categories[category_id]

    def create_product(self, name: str, category_id: int, description: str = "",
                       product_id: int | None = None) -> Product:
        category = self.categories[category_id]
        new_id = product_id or self._next_id(self.products)
        product = Product(new_id, name, category, description)
        self.products[new_id] = product
        return product

    def get_product(self, product_id: int) -> Product | None:
        return self.products.get(product_id)

    def update_product(self, product_id: int, **changes: Any) -> Product:
        product = self.products[product_id]
        if "category_id" in changes:
            product.category = self.categories[changes["category_id"]]
        for field_name in ("name", "description"):
            if field_name in changes:
                setattr(product, field_name, changes[field_name])
        return product

    def delete_product(self, product_id: int) -> None:
        del self.products[product_id]
        self.prices = [price for price in self.prices
                       if price.product.id != product_id]
        for user in self.users.values():
            user.remove_favorite(product_id)

    def create_store(self, name: str, url: str, store_id: int | None = None) -> Store:
        new_id = store_id or self._next_id(self.stores)
        store = Store(new_id, name, url)
        self.stores[new_id] = store
        return store

    def get_store(self, store_id: int) -> Store | None:
        return self.stores.get(store_id)

    def update_store(self, store_id: int, **changes: str) -> Store:
        store = self.stores[store_id]
        for field_name in ("name", "url"):
            if field_name in changes:
                setattr(store, field_name, changes[field_name])
        return store

    def delete_store(self, store_id: int) -> None:
        del self.stores[store_id]
        self.prices = [price for price in self.prices
                       if price.store.id != store_id]

    def create_price(self, product_id: int, store_id: int, price: float, url: str,
                     updated_at: datetime | None = None) -> Price:
        item = Price(self.products[product_id], self.stores[store_id], price, url,
                     updated_at or datetime.now())
        self.prices.append(item)
        return item

    def get_prices(self, product_id: int | None = None) -> list[Price]:
        if product_id is None:
            return list(self.prices)
        return [item for item in self.prices if item.product.id == product_id]

    def update_price(self, item: Price, **changes: Any) -> Price:
        if "product_id" in changes:
            item.product = self.products[changes["product_id"]]
        if "store_id" in changes:
            item.store = self.stores[changes["store_id"]]
        for field_name in ("price", "url", "updated_at"):
            if field_name in changes:
                setattr(item, field_name, changes[field_name])
        return item

    def delete_price(self, price: Price) -> None:
        self.prices.remove(price)

    def create_user(self, name: str, email: str, user_id: int | None = None) -> User:
        new_id = user_id or self._next_id(self.users)
        user = User(new_id, name, email)
        self.users[new_id] = user
        return user

    def get_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    def update_user(self, user_id: int, **changes: str) -> User:
        user = self.users[user_id]
        for field_name in ("name", "email"):
            if field_name in changes:
                setattr(user, field_name, changes[field_name])
        return user

    def delete_user(self, user_id: int) -> None:
        del self.users[user_id]

    def save(self, data_dir: Path) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        _write_json(data_dir, "products.json", {
            "categories": [item.to_dict() for item in self.categories.values()],
            "products": [item.to_dict() for item in self.products.values()],
        })
        _write_json(data_dir, "stores.json",
                    [item.to_dict() for item in self.stores.values()])
        _write_json(data_dir, "prices.json", [item.to_dict() for item in self.prices])
        _write_json(data_dir, "users.json", [item.to_dict() for item in self.users.values()])


def _read_json(data_dir: Path, filename: str) -> Any:
    with (data_dir / filename).open(encoding="utf-8") as file:
        return json.load(file)


def _write_json(data_dir: Path, filename: str, data: Any) -> None:
    with (data_dir / filename).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_data(data_dir: Path) -> dict[str, Any]:
    """Загружает JSON и связывает записи в коллекции объектов."""
    product_data = _read_json(data_dir, "products.json")
    categories = {item["id"]: Category.from_dict(item)
                  for item in product_data["categories"]}
    products = {item["id"]: Product.from_dict(item, categories)
                for item in product_data["products"]}
    stores = {item["id"]: Store.from_dict(item)
              for item in _read_json(data_dir, "stores.json")}
    prices = [Price.from_dict(item, products, stores)
              for item in _read_json(data_dir, "prices.json")]
    users = {item["id"]: User.from_dict(item, products)
             for item in _read_json(data_dir, "users.json")}
    return {"categories": categories, "products": products, "stores": stores,
            "prices": prices, "users": users}


def save_data(data_dir: Path, data: dict[str, Any]) -> None:
    """Сохраняет коллекции объектов в исходный набор JSON-файлов."""
    DataRepository(**data).save(data_dir)
