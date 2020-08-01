from tests.integration.integration_base_test import IntegrationBaseTest

from models.coupons import CouponModel


class TestCouponModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = CouponModel
        self.test_passing_param = {"code": self.coupon_params.get("code")}
        self.test_failing_param = {"code": "DUMMY20"}
        self.params = self.coupon_params

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_products_relationship(self):
        with self.app_context():
            coupon = CouponModel(**self.params)
            coupon.save_to_db()

            self.assertEqual(coupon.products, [])
