import pytest
import uuid
import random

from decimal import Decimal

from warehouse_management.domain.models import OrderItem

@pytest.fixture
def generate_random_item():
    return {
        "product_name": f"test_product_{uuid.uuid4()}",
        "quantity": random.randint(1, 50),
        "unit_price": Decimal(f"{random.uniform(1.00, 99.99):.2f}"),
    }

@pytest.fixture
def bunch_of_items():
    return (
        {
            "product_name": "test_product_1",
            "quantity": 2,
            "unit_price": Decimal(200.44),
        },
        {
            "product_name": "test_product_2",
            "quantity": 10,
            "unit_price": Decimal(599.99),
        },
        {
            "product_name": "test_product_3",
            "quantity": 1,
            "unit_price": Decimal(150),
        }
    )

@pytest.fixture
def order_items(bunch_of_items):
    return [OrderItem(**item) for item in bunch_of_items]

