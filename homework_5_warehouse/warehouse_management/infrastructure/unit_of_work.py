from warehouse_management.domain.unit_of_work import UnitOfWork
from warehouse_management.domain.repositories import InMemoryOrderRepository, InMemoryProductRepository


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.product_repo = InMemoryProductRepository()
        self.order_repo = InMemoryOrderRepository()
        self._committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.rollback()
        return False


    def rollback(self):
        self._committed = False

    def commit(self):
        self._committed = True

    @property
    def products(self):
        return self.product_repo

    @property
    def orders(self):
        return self.order_repo



