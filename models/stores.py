from dataclasses import dataclass
from typing import Any


@dataclass
class Store:
    id: int
    name: str
    url: str

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "url": self.url}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Store":
        return cls(int(data["id"]), str(data["name"]), str(data["url"]))
