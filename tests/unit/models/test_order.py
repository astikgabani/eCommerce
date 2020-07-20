from unittest.mock import MagicMock, PropertyMock, patch

from tests.unit.unit_base_test import UnitBaseTest

import models.order

from datetime import datetime, timedelta


class TestOrderModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "status": models.order.OrderStatusEnum.placed,
            "shipping_cost": 20,
            "total": 50,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.order.OrderModel(**self.params)

    # @patch("models.cart.CartModel.count_total", new_callable=PropertyMock)
    def test_pre_save(self):
        # Configure
        mock_cart = self.obj.cart = PropertyMock()
        mock_cart.count_total = 20
        self.obj.shipping_cost = 50

        # Execute
        self.obj.post_save()

        # Assert
        self.assertEqual(self.obj.total, 70)

    def test_deactivate(self):
        # Execute
        self.obj.deactivate()

        # Assert
        self.assertEqual(self.obj.status, models.order.OrderStatusEnum.cancelled)


class TestOrderReceiverModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "first_name": "Astik",
            "last_name": "Gabani",
            "phone_no": 9999559955,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.order.OrderReceiverModel(**self.params)

    def test_pre_save(self):
        # Execute
        self.obj.pre_save()
