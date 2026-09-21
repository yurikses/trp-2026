from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass
class Category:
    id: int
    name: str

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Category":
        return cls(int(data["id"]), str(data["name"]))


@dataclass
class Product:
    id: int
    name: str
    category: Category
    description: str = ""

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category.id,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], categories: dict[int, Category]) -> "Product":
        category_id = int(data["category_id"])
        return cls(int(data["id"]), str(data["name"]), categories[category_id],
                   str(data.get("description", "")))


def search_products(products: Iterable[Product], query: str) -> list[Product]:
    """Возвращает товары, содержащие запрос в названии."""
    normalized_query = query.strip().casefold()
    return [product for product in products
            if normalized_query in product.name.casefold()]
