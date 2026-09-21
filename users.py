from dataclasses import dataclass, field
from typing import Any

from products import Product


@dataclass
class User:
    id: int
    name: str
    email: str
    favorites: list[Product] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

    def add_favorite(self, product: Product) -> None:
        if product not in self.favorites:
            self.favorites.append(product)

    def remove_favorite(self, product_id: int) -> None:
        self.favorites = [product for product in self.favorites
                          if product.id != product_id]

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "email": self.email,
                "favorites": [product.id for product in self.favorites]}

    @classmethod
    def from_dict(cls, data: dict[str, Any], products: dict[int, Product]) -> "User":
        favorites = [products[int(product_id)]
                     for product_id in data.get("favorites", [])]
        return cls(int(data["id"]), str(data["name"]), str(data["email"]), favorites)
