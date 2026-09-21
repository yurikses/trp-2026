from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from products import Product
from stores import Store


@dataclass
class Price:
    product: Product
    store: Store
    price: float
    url: str
    updated_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"{self.product.name}: {self.price} ₽ ({self.store.name})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product.id,
            "store_id": self.store.id,
            "price": self.price,
            "url": self.url,
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], products: dict[int, Product],
                  stores: dict[int, Store]) -> "Price":
        return cls(products[int(data["product_id"])], stores[int(data["store_id"])],
                   float(data["price"]), str(data["url"]),
                   datetime.fromisoformat(data["updated_at"]))


def compare_prices(prices: Iterable[Price], product: Product) -> list[Price]:
    """Возвращает цены выбранного товара от самой низкой к высокой."""
    return sorted((item for item in prices if item.product.id == product.id),
                  key=lambda item: item.price)
