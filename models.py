from typing import Dict
from dataclasses import dataclass


class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        return self.quantity >= quantity

    def buy(self, quantity):
        if quantity <= 0:
            raise ValueError('Количество товаров для продажи может быть только положительным числом')
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError('Количества товара на остатках недостаточно для продажи')

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: Dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count <= 0:
            raise ValueError('Количество товара должно быть положительным числом')
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        # если продукта нет в корзине, то удалять нечего
        if product not in self.products:
            return
        if remove_count is None:
            self.products.pop(product)
        else:
            if remove_count <= 0:
                raise ValueError('Количество товара для удаления должно быть положительным числом')
            if self.products[product] <= remove_count:
                self.products.pop(product)
            else:
                self.products[product] -= remove_count

    def clear(self):
        self.products = {}

    def get_total_price(self) -> float:
        total_price = 0
        for product, count in self.products.items():
            total_price += product.price * count
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if not self.products:
            raise ValueError("Корзина пуста, нет товаров для продажи")

        for product, count in self.products.items():
            if not product.check_quantity(count):
                raise ValueError(
                    f"Количество товара {product.name} не хватает на складе. Остаток на складе {product.quantity}")

        for product, count in self.products.items():
            product.buy(count)
        self.clear()
