import pytest
import uuid
import random

from decimal import Decimal

from warehouse_management.domain.models import OrderItem
from warehouse_management.domain.services import WarehouseService


from warehouse_management.domain.models import ProductCategory


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

@pytest.fixture
def product_mock_repo(mocker):
    product_mock_repo = mocker.Mock()
    return product_mock_repo

@pytest.fixture
def order_mock_repo(mocker):
    order_mock_repo = mocker.Mock()
    return order_mock_repo

@pytest.fixture
def test_category():
    return ProductCategory(name='test_category')

@pytest.fixture
def warehouse_service(product_mock_repo, order_mock_repo):
    return WarehouseService(
        product_repo=product_mock_repo,
        order_repo=order_mock_repo,
    )