from datetime import datetime
from typing import List, Dict, Optional


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Store:
    def __init__(self, id: int, name: str, url: str):
        self.id = id
        self.name = name
        self.url = url


class Product:
    def __init__(self, id: int, name: str, category: Category):
        self.id = id
        self.name = name
        self.category = category
        self.description = ""


class Price:
    def __init__(self, product: Product, store: Store, price: float, url: str):
        self.product = product
        self.store = store
        self.price = price
        self.url = url
        self.updated_at = datetime.now()


class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.favorites: List[Product] = []


class PriceCompareSystem:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.products: Dict[int, Product] = {}
        self.stores: Dict[int, Store] = {}
        self.prices: List[Price] = []
        self.categories: Dict[int, Category] = {}
        self.current_user: Optional[User] = None

        self._initialize_data()

    def _initialize_data(self):
        """Инициализация тестовых данных"""
        
        self.categories[1] = Category(1, "Электроника")
        self.categories[2] = Category(2, "Бытовая техника")

        self.stores[1] = Store(1, "М.Видео", "https://mvideo.ru")
        self.stores[2] = Store(2, "Эльдорадо", "https://eldorado.ru")
        self.stores[3] = Store(3, "DNS", "https://dns-shop.ru")

        self.products[1] = Product(1, "iPhone 15", self.categories[1])
        self.products[2] = Product(2, "Samsung Galaxy S24", self.categories[1])
        self.products[3] = Product(3, "Холодильник LG", self.categories[2])

        self.prices.extend([
            Price(self.products[1], self.stores[1], 89990, "https://mvideo.ru/iphone15"),
            Price(self.products[1], self.stores[2], 87990, "https://eldorado.ru/iphone15"),
            Price(self.products[1], self.stores[3], 88500, "https://dns-shop.ru/iphone15"),
            Price(self.products[2], self.stores[1], 79990, "https://mvideo.ru/galaxy-s24"),
            Price(self.products[2], self.stores[2], 78990, "https://eldorado.ru/galaxy-s24"),
            Price(self.products[3], self.stores[1], 45990, "https://mvideo.ru/lg-fridge"),
            Price(self.products[3], self.stores[3], 44500, "https://dns-shop.ru/lg-fridge"),
        ])

    def search_products(self, query: str) -> List[Product]:
        """Поиск товаров по названию"""
        return [p for p in self.products.values() if query.lower() in p.name.lower()]

    def compare_prices(self, product: Product) -> List[Price]:
        """Сравнение цен на товар"""
        product_prices = [p for p in self.prices if p.product.id == product.id]
        return sorted(product_prices, key=lambda x: x.price)

    def add_to_favorites(self, product: Product):
        """Добавление товара в избранное"""
        if self.current_user and product not in self.current_user.favorites:
            self.current_user.favorites.append(product)
            print(f"Товар '{product.name}' добавлен в избранное")

    def show_favorites(self):
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

    def print_prices(self, prices: List[Price]):
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


def main():
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
            product_id = int(input("Введите ID товара: "))
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
