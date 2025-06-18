import dataclasses
import json

from typing import List
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum
from decimal import Decimal

@dataclasses.dataclass
class ProductCategory:
    name:str
    id: Optional[UUID] = None

class OrderStatus(Enum):
    NEW = 'new'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


@dataclasses.dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float
    category: ProductCategory

    def __post_init__(self):
        if self.price < 0:
            raise ValueError('Unit price cannot be negative')
        if self.quantity < 0:
            raise ValueError('Quantity cannot be negative')


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "category": str(self.category.id) if self.category.id else None
        }

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "quantity": self.quantity,
                "price": self.price,
                "category": {
                    "id": str(self.category.id) if self.category.id else None,
                    "name": self.category.name,
                }
            }
        )

@dataclasses.dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: Decimal
    sub_total: Decimal = dataclasses.field(init=False)


    def __post_init__(self):
        if self.unit_price < 0:
            raise ValueError('Unit price cannot be negative')
        if self.quantity < 0:
            raise ValueError('Quantity cannot be negative')
        self.sub_total = Decimal(self.quantity * self.unit_price)





@dataclasses.dataclass
class Order:
    id: UUID
    status: OrderStatus = OrderStatus.NEW
    items: List[OrderItem] = dataclasses.field(default_factory=list)
    _ACCEPTED_STATUSES = {
        OrderStatus.NEW: (OrderStatus.PROCESSING, OrderStatus.CANCELED),
        OrderStatus.PROCESSING: (OrderStatus.SHIPPED, OrderStatus.CANCELED),
        OrderStatus.SHIPPED: (OrderStatus.DELIVERED,)
    }

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if not self.items:
            raise ValueError('Cannot create order without products')


    def change_status(self, new_status):
        approved_status = self._ACCEPTED_STATUSES.get(self.status)
        if not approved_status:
            raise ValueError(
                "Status value doesn't found among Accepted Statuses"
            )

        if new_status in approved_status:
            self.status = new_status
        else:
            raise ValueError(
                f"Current status {self.status} cannot be changed to {new_status}."
                f"Avaialable options: {self._ACCEPTED_STATUSES.get(self.status)}"
            )

    def add_item(self, item: OrderItem):
        self.items.append(item)

    @property
    def total_amount(self) -> Decimal:
        return sum(item.sub_total for item in self.items)


@dataclasses.dataclass
class Warehouse:
    id: UUID
    name: str
    address: str
    location: str
    capacity: int


