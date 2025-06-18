from uuid import UUID

from abc import ABC, abstractmethod
from typing import List
from .models import Product, Order, Warehouse

class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        pass

    @abstractmethod
    def get(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def list(self) -> List[Product]:
        pass

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        pass

    @abstractmethod
    def get(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def list(self) -> List[Order]:
        pass

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders = []

    def add(self, order: Order):
        self._orders.append(order)

    def get(self, order_id):
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def list(self):
        return self._orders


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._products = []

    def add(self, product: Product):
        self._products.append(product)

    def get(self, product_id):
        for product in self._products:
            if product.id == product_id:
                return product
        return None

    def list(self):
        return self._products


