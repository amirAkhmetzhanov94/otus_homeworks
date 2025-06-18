from warehouse_management.domain.repositories import ProductRepository, OrderRepository

from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @property
    @abstractmethod
    def products(self) -> ProductRepository:
        pass

    @property
    @abstractmethod
    def orders(self) -> OrderRepository:
        pass
