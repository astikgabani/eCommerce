from tests.integration.integration_base_test import IntegrationBaseTest

from models.cart import CartModel, CartItemsModel
from models.users import UserModel, UserSessionModel
from models.coupons import CouponModel
from models.products import (
    ProductModel,
    ProductAttributeModel,
    ProductAttributeOptionsModel,
)


class TestCartModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = CartModel
        self.params = self.cart_params
        # total should be 0 even if we set total = 100 . bcz in pre_save method, count will be calculated
        self.test_passing_param = {"total": 0.0}
        self.test_failing_param = {"total": 100.0}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_user_relationship(self):
        with self.app_context():
            user = UserModel(**self.user_params)
            user.save_to_db()

            cart = CartModel(user_id=user.id, **self.params)
            cart.save_to_db()

            self.assertEqual(cart.user.email, self.user_params.get("email"))

    def test_coupon_relationship(self):
        with self.app_context():
            coupon = CouponModel(**self.coupon_params)
            coupon.save_to_db()

            cart = CartModel(coupon_id=coupon.id, **self.params)
            cart.save_to_db()

            self.assertEqual(cart.coupon.code, self.coupon_params.get("code"))

    def test_session_relationship(self):
        with self.app_context():
            session = UserSessionModel(**self.user_session_params)
            session.save_to_db()

            cart = CartModel(session_id=session.id, **self.params)
            cart.save_to_db()

            self.assertEqual(cart.session.ip, self.user_session_params.get("ip"))


class TestCartItemsModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = CartItemsModel
        with self.app_context():
            cart = CartModel(**self.cart_params)
            cart.save_to_db()

            product = ProductModel(**self.product_params)
            product.save_to_db()

            product_attr = ProductAttributeModel(
                product_id=product.id, **self.product_attr_params
            )
            product_attr.save_to_db()

            product_attr_opt = ProductAttributeOptionsModel(
                attr_id=product_attr.id, **self.product_attr_options_params
            )
            product_attr_opt.save_to_db()

            self.params = self.cart_item_params
            self.params.update(
                {
                    "cart_id": cart.id,
                    "product_id": product.id,
                    "attr_option_id": product_attr_opt.id,
                }
            )

        # total should be 0 even if we set total = 100 . bcz in pre_save method, count will be calculated
        self.test_passing_param = {"quantity": self.cart_item_params.get("quantity")}
        self.test_failing_param = {"quantity": 0}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_session_product_attrOption_relationship(self):
        with self.app_context():

            cart_item = CartItemsModel(**self.params)
            cart_item.save_to_db()

            self.assertIsNotNone(cart_item.cart.id)
            self.assertEqual(cart_item.product.slug, self.product_params.get("slug"))
            self.assertEqual(
                cart_item.product_option.name,
                self.product_attr_options_params.get("name"),
            )
