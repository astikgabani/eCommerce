from tests.base_test import BaseTest, app

from models.users import UserModel, UserConfirmationModel, UserRoleModel
from models.coupons import CouponModel

import json


class SystemBaseTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.headers = {"Content-Type": "application/json"}

    def create_coupon(self):
        with app.app_context():
            coupon = CouponModel(**self.coupon_params)
            coupon.save_to_db()
            return coupon.get_json_data()

    def add_product_to_cart(self, product_id, attr_option_id=None):
        with app.test_client() as client:
            with app.app_context():
                data = self.cart_item_params.copy()
                data.update(
                    {"product_id": product_id, "attr_option_id": attr_option_id}
                )
                response = client.post(
                    "/cart-item", data=json.dumps(data), headers=self.headers,
                )
                self.assertEqual(response.status_code, 200)
                return json.loads(response.data)["data"]

    def create_product(self):
        product_dict_param = {
            "products": [
                {
                    "name": "shirts",
                    "description": "Awesome Shirts",
                    "price": 100,
                    "attrs": [
                        {
                            "name": "color",
                            "attrs_options": [
                                {"name": "Red", "value": "red", "price_change": 10},
                                {"name": "Blue", "value": "blue", "price_change": 5},
                            ],
                        }
                    ],
                }
            ]
        }
        with app.test_client() as client:
            with app.app_context():
                response = client.post(
                    "/products",
                    data=json.dumps(product_dict_param),
                    headers=self.headers,
                )
                self.assertEqual(response.status_code, 200)
                return json.loads(response.data)["created_products"][0]

    def set_session_key(self):
        self.register_endpoint = "/register"
        self.login_endpoint = "/login"
        with app.test_client() as client:
            with app.app_context():
                user = UserModel(**self.user_params)
                user.save_to_db()

                confirmation = UserConfirmationModel(
                    **{"confirmed": True, "user_id": user.id}
                )
                confirmation.save_to_db()

                response = client.post(
                    self.login_endpoint,
                    data=json.dumps(
                        {
                            "email": self.user_params.get("email"),
                            "password": self.user_params.get("password"),
                        }
                    ),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(response.data)

                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]

                self.headers.update({"Authorization": f"Bearer {self.access_token}"})
                self.refresh_token_headers = self.headers.copy()
                self.refresh_token_headers.update(
                    {"Authorization": f"Bearer {self.refresh_token}"}
                )

    def get_admin_account(self):
        self.set_session_key()
        role = UserRoleModel(**self.user_roles_params)
        role.save_to_db()

        user = UserModel.get_item(first_name=self.user_params.get("first_name"))
        user.roles.append(role)
        user.save_to_db()
