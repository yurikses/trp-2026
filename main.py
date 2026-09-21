from pathlib import Path

from prices import Price, compare_prices
from products import Product, search_products
from storage import DataRepository, load_data
from users import User


class PriceCompareSystem:
    def __init__(self) -> None:
        self.current_user: User | None = None

        data = load_data(Path(__file__).parent / "data")
        self.repository = DataRepository(**data)
        self.categories = self.repository.categories
        self.stores = self.repository.stores
        self.products = self.repository.products
        self.prices = self.repository.prices
        self.users = self.repository.users

    def search_products(self, query: str) -> list[Product]:
        """Поиск товаров по названию"""
        return search_products(self.products.values(), query)

    def compare_prices(self, product: Product) -> list[Price]:
        """Сравнение цен на товар"""
        return compare_prices(self.prices, product)

    def add_to_favorites(self, product: Product) -> None:
        """Добавление товара в избранное"""
        if self.current_user and product not in self.current_user.favorites:
            self.current_user.add_favorite(product)
            print(f"Товар '{product.name}' добавлен в избранное")

    def show_favorites(self) -> None:
        """Показать избранное"""
        if not self.current_user:
            print("Пользователь не авторизован")
            return

        if not self.current_user.favorites:
            print("Избранное пусто")
            return

        print("\n=== Избранное ===")
        for i, product in enumerate(self.current_user.favorites, 1):
            print(f"{i}. {product.name} ({product.category.name})")

    def print_prices(self, prices: list[Price]) -> None:
        """Вывод цен в отформатированном виде"""
        if not prices:
            print("Цены не найдены")
            return

        print(f"\n{'Магазин':<20} {'Цена':>12} {'Ссылка':<30}")
        print("-" * 65)
        for p in prices:
            print(f"{p.store.name:<20} {p.price:>10,} ₽ {p.url:<30}")
        print("-" * 65)
        if prices:
            print(f"Лучшая цена: {prices[0].price:,} ₽ в {prices[0].store.name}")


def main() -> None:
    system = PriceCompareSystem()

    while True:
        print("\n" + "=" * 40)
        print("PriceCompare - Система сравнения цен")
        print("=" * 40)
        print("1. Поиск товара")
        print("2. Сравнить цены")
        print("3. Показать категории")
        print("4. Избранное")
        print("5. Выход")
        print("=" * 40)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            query = input("Введите название товара: ")
            products = system.search_products(query)

            if not products:
                print("Товары не найдены")
                continue

            print("\nНайдены товары:")
            for i, p in enumerate(products, 1):
                print(f"{i}. {p.name} ({p.category.name})")

        elif choice == "2":
            try:
                product_id = int(input("Введите ID товара: "))
            except ValueError:
                print("ID товара должен быть числом")
                continue
            if product_id in system.products:
                product = system.products[product_id]
                prices = system.compare_prices(product)
                system.print_prices(prices)

                fav = input("Добавить в избранное? (y/n): ")
                if fav.lower() == 'y':
                    system.add_to_favorites(product)
            else:
                print("Товар не найден")

        elif choice == "3":
            print("\nКатегории:")
            for cat in system.categories.values():
                print(f"- {cat.name}")

        elif choice == "4":
            system.show_favorites()

        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
