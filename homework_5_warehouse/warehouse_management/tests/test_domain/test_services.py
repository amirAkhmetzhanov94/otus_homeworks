import pytest

from warehouse_management.domain.services import WarehouseService
from warehouse_management.domain.models import ProductCategory, OrderStatus
from warehouse_management.infrastructure.unit_of_work import InMemoryUnitOfWork

def test_warehouse_service_create_product(
    product_mock_repo,
    test_category,
    warehouse_service,
):

    test_product = warehouse_service.create_product(
        name="test_product",
        quantity=3,
        price=3.50,
        category=test_category
    )

    product_mock_repo.add.assert_called_once_with(test_product)
    assert test_product.name == 'test_product'
    assert test_product.category == test_category

def test_warehouse_service_create_product_with_negative_price_raises(
    product_mock_repo,
    test_category,
    warehouse_service,
):
    with pytest.raises(ValueError):
        test_product = warehouse_service.create_product(
            name="test_product",
            quantity=3,
            price=-1,
            category=test_category
        )

    product_mock_repo.add.assert_not_called()

def test_warehouse_service_create_product_with_negative_quantity_raises(
    product_mock_repo,
    test_category,
    warehouse_service,
):
    with pytest.raises(ValueError):
        test_product = warehouse_service.create_product(
            name="test_product",
            quantity=-1,
            price=1.99,
            category=test_category
        )

    product_mock_repo.add.assert_not_called()


def test_warehouse_service_create_order(
    order_mock_repo,
    warehouse_service,
    order_items,
):
    test_order = warehouse_service.create_order(
        status=OrderStatus.NEW,
        products=order_items,
    )

    order_mock_repo.add.assert_called_once_with(test_order)
    assert test_order.status == OrderStatus.NEW
    assert test_order.items == order_items


def test_warehouse_service_create_order_with_empty_products_raises(
    order_mock_repo,
    warehouse_service,
    order_items,
):
    with pytest.raises(ValueError):
        test_order = warehouse_service.create_order(
            status=OrderStatus.NEW,
            products=[],
        )

    order_mock_repo.add.assert_not_called()


def test_in_memory_unit_of_work_commit():
    with InMemoryUnitOfWork() as test_uow:
        test_uow.commit()

    assert test_uow._committed is True

def test_in_memory_unit_of_work_rollback():
    with InMemoryUnitOfWork() as test_uow:
        test_uow.rollback()

    assert test_uow._committed is False

def test_in_memory_unit_of_work_rollback_on_error(
    warehouse_service,
    order_items,
):
    test_order = warehouse_service.create_order(
        status=OrderStatus.NEW,
        products=order_items,
    )
    with pytest.raises(ValueError):
        with InMemoryUnitOfWork() as test_uow:
            test_uow.orders.add(test_order)
            raise ValueError("Rollback on error")
    assert test_uow._committed is False



def test_in_memory_unit_of_work_add_order(
    warehouse_service,
    order_items,
):
    with InMemoryUnitOfWork() as test_uow:
        test_order = warehouse_service.create_order(
            status=OrderStatus.NEW,
            products=order_items,
        )
        test_uow.orders.add(test_order)

        actual = test_uow.orders.get(test_order.id)
        expected = test_order

        assert actual == expected

def test_in_memory_unit_of_work_add_product(
    warehouse_service,
    order_items,
    test_category,

):
    with InMemoryUnitOfWork() as test_uow:
        test_product = warehouse_service.create_product(
            name="test_product",
            quantity=3,
            price=3.50,
            category=test_category
        )
        test_uow.products.add(test_product)

        actual = test_uow.products.get(test_product.id)
        expected = test_product

        assert actual == expected

