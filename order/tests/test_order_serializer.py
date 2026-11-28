import pytest

from order.factories import OrderFactory
from order.serializers import OrderSerializer
from product.factories import ProductFactory


@pytest.mark.django_db
def test_order_serializer_returns_total():
    product1 = ProductFactory(price=100)
    product2 = ProductFactory(price=50)

    order = OrderFactory(product=[product1, product2])

    serializer = OrderSerializer(order)

    assert serializer.data["total"] == 150


@pytest.mark.django_db
def test_order_serializer_returns_total_with_null_price():
    product1 = ProductFactory(price=100)
    product2 = ProductFactory(price=None)

    order = OrderFactory(product=[product1, product2])

    serializer = OrderSerializer(order)

    assert serializer.data["total"] == 100


@pytest.mark.django_db
def test_order_serializer_returns_products():
    product1 = ProductFactory()
    product2 = ProductFactory()

    order = OrderFactory(product=[product1, product2])

    serializer = OrderSerializer(order)

    assert len(serializer.data["product"]) == 2


@pytest.mark.django_db
def test_order_serializer_accepts_valid_data():
    data = {
        "product": [
            {
                "title": "Teclado",
                "description": "Teclado mecânico",
                "price": 150,
                "active": True,
                "category": [
                    {
                        "title": "Eletrônicos",
                        "slug": "eletronicos",
                        "description": "Produtos eletrônicos",
                        "active": True,
                    }
                ],
            }
        ]
    }

    serializer = OrderSerializer(data=data)

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_order_serializer_requires_product():
    serializer = OrderSerializer(data={})

    assert not serializer.is_valid()
    assert "product" in serializer.errors


@pytest.mark.django_db
def test_order_serializer_rejects_invalid_product():
    data = {
        "product": [
            {
                "title": "Teclado",
                "price": -50,
                "category": [
                    {
                        "title": "Eletrônicos",
                        "slug": "eletronicos",
                    }
                ],
            }
        ]
    }

    serializer = OrderSerializer(data=data)

    assert not serializer.is_valid()
    assert "product" in serializer.errors