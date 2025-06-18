from typing import List
from .models import Product, Order, ProductCategory, OrderStatus, OrderItem
from .repositories import ProductRepository, OrderRepository

class WarehouseService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository):
        self.product_repo=product_repo
        self.order_repo=order_repo

    def create_product(self, name: str, quantity: int, price: float, category: ProductCategory) -> Product:
        product=Product(id=None, name=name, quantity=quantity, price=price, category=category)
        self.product_repo.add(product)
        return product

    def create_order(self, products: List[OrderItem], status: OrderStatus) -> Order:
        order=Order(id=None, items=products, status=status)
        self.order_repo.add(order)
        return order
