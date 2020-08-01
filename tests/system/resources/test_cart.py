from tests.system.system_base_test import SystemBaseTest

import json


class TestCartResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/cart"

    def test_get_without_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(self.endpoint)
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertIsNone(resp_data["data"]["user_id"])

    def test_get_with_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.get(self.endpoint, headers=self.headers)
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertIsNotNone(resp_data["data"]["user_id"])

    def test_post_with_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.post(self.endpoint, headers=self.headers)
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertIsNotNone(resp_data["data"]["user_id"])

    def test_delete_without_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Config
                client.get(self.endpoint)

                # Execute
                response = client.delete(self.endpoint)

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_delete_with_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()
                client.get(self.endpoint, headers=self.headers)

                # Execute
                response = client.delete(self.endpoint, headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_delete_without_session_key_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.delete(self.endpoint)

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_delete_with_session_key_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.delete(self.endpoint, headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 404)


class TestCartItemResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/cart-item"

    def test_get_added_cart_item(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = self.cart_item_params
                data.update(
                    {
                        "product_id": product["id"],
                        "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                    }
                )
                client.post(self.endpoint, data=json.dumps(data), headers=self.headers)

                # Execute
                response = client.get(self.endpoint, headers=self.headers)
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsInstance(resp_data["data"], list)

    def test_post_product_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(
                    self.endpoint,
                    data=json.dumps({"product_id": 1}),
                    headers=self.headers,
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_post_added_cart_item(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = self.cart_item_params
                data.update(
                    {
                        "product_id": product["id"],
                        "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                    }
                )

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])

    def test_post_already_added_cart_item(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = self.cart_item_params
                data.update(
                    {
                        "quantity": 1,
                        "product_id": product["id"],
                        "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                    }
                )
                client.post(self.endpoint, data=json.dumps(data), headers=self.headers)
                data.update({"quantity": 5})

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertEqual(resp_data["data"]["quantity"], 6)

    def test_post_quantity_should_not_zero(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = {}
                data.update(
                    {
                        "product_id": product["id"],
                        "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                    }
                )

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 400)

    def test_put_updated(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = {}
                data.update(
                    {
                        "product_id": product["id"],
                        "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                    }
                )
                client.post(self.endpoint, data=json.dumps(data), headers=self.headers)
                data.update({"quantity": 10})

                # Execute
                response = client.put(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertEqual(resp_data["data"]["quantity"], 10)

    def test_put_product_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = {
                    "product_id": product["id"],
                    "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                }

                # Execute
                response = client.put(
                    self.endpoint, data=json.dumps(data), headers=self.headers,
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_deleted(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = {
                    "product_id": product["id"],
                    "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                }
                client.post(self.endpoint, data=json.dumps(data), headers=self.headers)

                # Execute
                response = client.delete(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_delete_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                data = {
                    "product_id": product["id"],
                    "attr_option_id": product["attrs"][0]["attrs_options"][0]["id"],
                }

                # Execute
                response = client.delete(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)


class TestApplyCouponResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.coupon = self.create_coupon()
        self.endpoint = f"/apply-coupon/{self.coupon.get('code')}"

    def test_post_without_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(self.endpoint)

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_coupon_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()
                self.endpoint = "/apply-coupon/DUMMY"

                # Execute
                response = client.post(self.endpoint, headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_post_cart_should_not_be_empty(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.post(self.endpoint, headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 400)

    def test_post_coupon_applied(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()
                product = self.create_product()
                self.add_product_to_cart(
                    product.get("id"),
                    attr_option_id=product["attrs"][0]["attrs_options"][0]["id"],
                )

                # Execute
                response = client.post(self.endpoint, headers=self.headers)
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["coupon_id"])


class TestMergeTwoCartResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/cart-merge/{}"

    def test_post_without_session_key(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(self.endpoint.format(1), headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_cart_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.post(self.endpoint.format(5), headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_post_cart_merged(self):
        with self.app() as client:
            with self.app_context():
                # Config
                product = self.create_product()
                cart = self.add_product_to_cart(
                    product.get("id"),
                    attr_option_id=product["attrs"][0]["attrs_options"][0]["id"],
                )
                self.set_session_key()

                # Execute
                response = client.post(
                    self.endpoint.format(cart.get("id")), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["user_id"])
                self.assertIsNotNone(resp_data["data"]["session_id"])
                self.assertNotEqual(resp_data["data"]["total"], 0)
