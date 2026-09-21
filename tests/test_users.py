from products import Category, Product
from users import User


def test_user_favorites_are_independent():
    first = User(1, "А", "a@example.com")
    second = User(2, "Б", "b@example.com")
    first.favorites.append(Product(1, "Товар", Category(1, "Категория")))

    assert second.favorites == []
