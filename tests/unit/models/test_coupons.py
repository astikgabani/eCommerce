from tests.unit.unit_base_test import UnitBaseTest

import models.coupons

from datetime import datetime, timedelta


class TestCouponModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "code": "CODE20",
            "type": models.coupons.CouponTypeEnum.percentage,
            "value": 20,
            "max_value": 50,
            "start": datetime.utcnow() - timedelta(days=5),
            "expire": datetime.utcnow() + timedelta(days=5),
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.coupons.CouponModel(**self.params)

    def test_pre_save(self):
        # Execute
        self.obj.pre_save()

    def test_get_discount_price(self):

        # Execute
        output = self.obj.get_discount_price(500)
        output_2 = self.obj.get_discount_price(200)

        # Assert
        self.assertEqual(output, 50, "get_discount_price, Discount price is not calculating properly.")
        self.assertEqual(output_2, 40, "get_discount_price, Discount price is not calculating properly.")

    def test_get_discount_price_expired_coupon(self):

        # Configure
        self.obj.expire = datetime.utcnow()

        # Execute
        output = self.obj.get_discount_price(500)

        # Assert
        self.assertEqual(output, 0, "get_discount_price, Discount price is not calculating if coupon has expired.")

    def test_get_discount_price_not_started_coupon(self):

        # Configure
        self.obj.start = datetime.utcnow() + timedelta(days=3)

        # Execute
        output = self.obj.get_discount_price(500)

        # Assert
        self.assertEqual(output, 0, "get_discount_price, Discount price is not calculating if coupon has expired.")

    def test_get_discount_price_value_discount(self):

        # Configure
        self.obj.type = models.coupons.CouponTypeEnum.price

        # Execute
        output = self.obj.get_discount_price(500)

        # Assert
        self.assertEqual(output, 20, "get_discount_price, Discount price is not calculating if coupon has expired.")
