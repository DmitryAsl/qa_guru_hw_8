import pytest

from models import Product
from models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def water():
    return Product("Water good", 100, "This is a good water", 100)


@pytest.fixture
def bread():
    return Product("Kybai", 33.3, 'Bread is head', 38)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000)
        assert product.check_quantity(999)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        product.buy(998)
        assert product.quantity == 2

        product.buy(2)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match='Количества товара на остатках недостаточно для продажи'):
            product.buy(1001)

    def test_product_buy_incorrect_quantity(self, product):
        with pytest.raises(ValueError, match='Количество товаров для продажи может быть только положительным числом'):
            product.buy(-1)
        with pytest.raises(ValueError, match='Количество товаров для продажи может быть только положительным числом'):
            product.buy(0)


class TestCart:

    def test_add_product_in_cart(self, cart, water, bread):
        cart.add_product(water)
        assert len(cart.products) == 1 and cart.products[water] == 1

        cart.add_product(water)
        assert len(cart.products) == 1 and cart.products[water] == 2

        cart.add_product(bread, 39)
        assert len(cart.products) == 2 and cart.products[bread] == 39

    def test_add_product_incorrect_quantity(self, cart, water):
        with pytest.raises(ValueError, match="Количество товара должно быть положительным числом"):
            cart.add_product(water, -1)
        with pytest.raises(ValueError, match="Количество товара должно быть положительным числом"):
            cart.add_product(water, 0)

    def test_remove_product_from_cart(self, cart, water, bread):
        cart.add_product(water, 3)
        cart.remove_product(water, 1)
        assert len(cart.products) == 1 and cart.products[water] == 2

        cart.remove_product(water)
        assert len(cart.products) == 0

        cart.add_product(water)
        cart.add_product(bread)
        cart.remove_product(water, 100000)
        assert len(cart.products) == 1 and cart.products[bread] == 1

        cart.remove_product(bread, 1)
        assert len(cart.products) == 0

        cart.add_product(water)
        cart.remove_product(bread)
        assert len(cart.products) == 1

    def test_remove_product_incorrect_quantity(self, cart, water):
        cart.add_product(water)
        with pytest.raises(ValueError, match='Количество товара для удаления должно быть положительным числом'):
            cart.remove_product(water, 0)
        with pytest.raises(ValueError, match="Количество товара для удаления должно быть положительным числом"):
            cart.remove_product(water, -1)

    def test_clear_cart(self, cart, water, bread):
        cart.clear()
        assert len(cart.products) == 0

        cart.add_product(water)
        cart.add_product(bread)
        cart.clear()
        assert len(cart.products) == 0

    def test_total_price_by_cart(self, cart, water, bread):
        assert cart.get_total_price() == 0

        cart.add_product(water, 3)
        cart.add_product(bread, 1)
        assert cart.get_total_price() == pytest.approx(333.3)

    def test_buy_products(self, cart, water, bread):
        cart.add_product(water)
        cart.add_product(bread, 38)
        cart.buy()
        assert len(cart.products) == 0
        assert water.quantity == 99 and bread.quantity == 0

        cart.add_product(water)
        cart.add_product(water, 98)
        cart.buy()
        assert len(cart.products) == 0
        assert water.quantity == 0

    def test_buy_empty_cart(self, cart):
        with pytest.raises(ValueError, match="Корзина пуста, нет товаров для продажи"):
            cart.buy()

    def test_buy_product_more_remains(self, cart, water, bread):
        cart.add_product(bread, 10)
        cart.add_product(water, 101)
        with pytest.raises(ValueError,
                           match=f"Количество товара {water.name} не хватает на складе. Остаток на складе {water.quantity}"):
            cart.buy()

        assert len(cart.products) == 2
        assert bread.quantity == 38 and water.quantity == 100
