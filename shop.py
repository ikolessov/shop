from typing import List


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} — {self.price:.2f} руб."

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price:.2f})"

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.price == other.price
        return False

    def __lt__(self, other):
        if isinstance(other, Product):
            return self.price < other.price
        return NotImplemented


class Discount:
    def __init__(self, description: str, discount_percent: float):
        self.description = description
        self.discount_percent = discount_percent

    def __str__(self):
        return f"Скидка: {self.description} ({self.discount_percent}%)"

    def __repr__(self):
        return f"Discount(description={self.description!r}, discount_percent={self.discount_percent})"

    @staticmethod
    def apply(price: float, discount_percent: float) -> float:
        """Применение скидки"""
        return price * (1 - discount_percent / 100)

    @staticmethod
    def seasonal_discount(price: float) -> float:
        return Discount.apply(price, 15)  # сезонная скидка 15%

    @staticmethod
    def promo_discount(price: float) -> float:
        return Discount.apply(price, 10)  # скидка по промокоду 10%


class Order:
    total_orders = 0
    total_sum = 0

    def __init__(self, products: List[Product]):
        self.products = products
        self.price = sum(p.price for p in products)
        Order.total_orders += 1
        Order.total_sum += self.price

    def apply_discount(self, discount: Discount):
        old_price = self.price
        self.price = Discount.apply(self.price, discount.discount_percent)
        return f"Применена {discount.description}: {old_price:.2f} → {self.price:.2f}"

    def __str__(self):
        return f"Заказ из {len(self.products)} товаров на сумму {self.price:.2f} руб."

    def __repr__(self):
        return f"Order(products={self.products!r})"

    @classmethod
    def get_total_orders(cls):
        return cls.total_orders

    @classmethod
    def get_total_sum(cls):
        return cls.total_sum


class Customer:
    def __init__(self, name: str):
        self.name = name
        self.orders: List[Order] = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def __str__(self):
        return f"Клиент {self.name}, заказов: {len(self.orders)}"

    def __repr__(self):
        return f"Customer(name={self.name!r}, orders={self.orders!r})"


# =================== ДЕМОНСТРАЦИЯ ===================

if __name__ == "__main__":
    # Создание продуктов
    p1 = Product("Ноутбук", 60000)
    p2 = Product("Смартфон", 30000)
    p3 = Product("Наушники", 5000)

    # Клиенты
    c1 = Customer("Андрей")
    c2 = Customer("Мария")

    # Заказы
    order1 = Order([p1, p3])  # ноутбук + наушники
    order2 = Order([p2])      # смартфон
    order3 = Order([p3, p3])  # два наушника

    # Добавляем заказы клиентам
    c1.add_order(order1)
    c2.add_order(order2)
    c2.add_order(order3)

    # Применение скидки
    discount1 = Discount("Сезонная скидка", 15)
    print(order1.apply_discount(discount1))

    # Вывод информации
    print(c1)
    print(c2)

    for o in c2.orders:
        print(o)

    # Общая статистика
    print(f"Всего заказов: {Order.get_total_orders()}")
    print(f"Общая сумма заказов: {Order.get_total_sum():.2f} руб.")
