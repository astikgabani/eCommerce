from unittest.mock import MagicMock, patch, PropertyMock

from tests.unit.unit_base_test import UnitBaseTest

import models.cart

from datetime import datetime


class TestCartModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.cart_params = {
            "id": 1,
            "total": 10.00,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
            "user_id": 1,
            "session_id": 1,
            "coupon_id": 1
            }
        self.cart_obj = models.cart.CartModel(**self.cart_params)

    @patch("models.cart.CartModel.count_total", new_callable=PropertyMock)
    def test_pre_save(self, count_total_mock):
        # configure
        count_total_mock.return_value = 20

        # Execute
        self.cart_obj.pre_save()

        # Assert
        self.assertEqual(self.cart_obj.total, 20, "pre_save, total is not updating.")
