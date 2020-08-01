from tests.integration.integration_base_test import IntegrationBaseTest

from models.order import OrderModel, OrderReceiverModel
from models.users import UserModel, UserSessionModel
from models.cart import CartModel


class TestOrderModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = OrderModel
        self.params = self.order_params
        with self.app_context():
            order_receiver = OrderReceiverModel(**self.order_receiver_params)
            order_receiver.save_to_db()

            user = UserModel(**self.user_params)
            user.save_to_db()

            cart = CartModel(user_id=user.id, **self.cart_params)
            cart.save_to_db()

            self.params.update(
                {
                    "order_receiver_id": order_receiver.id,
                    "cart_id": cart.id,
                    "user_id": user.id,
                }
            )

        self.test_passing_param = {"shipping_cost": 20.00}
        self.test_failing_param = {"shipping_cost": 0.0}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_user_relationship(self):
        with self.app_context():
            order = OrderModel(**self.params)
            order.save_to_db()

            self.assertEqual(order.user.email, self.user_params.get("email"))
            self.assertEqual(
                order.order_receiver.first_name,
                self.order_receiver_params.get("first_name"),
            )
            self.assertIsNotNone(order.cart.id)


class TestOrderReceiverModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = OrderReceiverModel
        self.params = self.order_receiver_params

        self.test_passing_param = {
            "first_name": self.order_receiver_params.get("first_name")
        }
        self.test_failing_param = {"first_name": ""}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()
