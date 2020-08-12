from tests.system.system_base_test import SystemBaseTest

import json


class TestOrderResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/order/{}"

    def test_get_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(
                    self.endpoint.format("NEW40"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_get_order(self):
        with self.app() as client:
            with self.app_context():
                # Config
                data = self.get_whole_order_data()
                order = self.create_order(**data)

                # Execute
                response = client.get(
                    self.endpoint.format(order.get("id")), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])
                self.assertEqual(resp_data["data"]["status"], "placed")

    def test_get_order_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.get(
                    self.endpoint.format("5rtr5"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_delete_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.delete(
                    self.endpoint.format("NEW40"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_delete_order(self):
        with self.app() as client:
            with self.app_context():
                # Config
                data = self.get_whole_order_data()
                order = self.create_order(**data)

                # Execute
                response = client.delete(
                    self.endpoint.format(order.get("id")), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 201)

    def test_delete_order_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.delete(
                    self.endpoint.format("5rtr5"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)


class TestOrdersResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/orders"

    def test_get_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(
                    self.endpoint, headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_get_orders(self):
        with self.app() as client:
            with self.app_context():
                # Config
                data = self.get_whole_order_data()
                order = self.create_order(**data)

                # Execute
                response = client.get(
                    self.endpoint, headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(str(resp_data["data"][0]["id"]), order.get("id"))
                self.assertEqual(resp_data["data"][0]["status"], "placed")


class TestOrderCreateResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/order"

    def test_post_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(
                    self.endpoint, headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_orders(self):
        with self.app() as client:
            with self.app_context():
                # Config
                data = self.get_whole_order_data()
                data.update({"is_testing_enable": True})

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 201)
                self.assertEqual(resp_data["data"]["status"], "placed")
                self.assertEqual(resp_data["data"]["payment_status"], "paid")

    def test_post_orders_cart_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                user = self.set_session_key()
                order_receiver = self.create_order_receiver()
                data = self.order_params.copy()
                data.update({
                    "order_receiver_id": order_receiver.get("id"),
                    "user_id": user.get("id")
                })

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_post_order_already_placed(self):
        with self.app() as client:
            with self.app_context():
                # Config
                data = self.get_whole_order_data()
                self.create_order(**data)

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 409)


class TestOrderReceiverResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/order-receiver/{}"

    def test_get_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(
                    self.endpoint.format(1), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_get_order_receiver_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.get(
                    self.endpoint.format(1), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_get_order_receiver(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()
                order_receiver = self.create_order_receiver()

                # Execute
                response = client.get(
                    self.endpoint.format(order_receiver.get("id")), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(str(resp_data["data"]["id"]), order_receiver.get("id"))

    def test_put_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.put(
                    self.endpoint.format(1), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_put_order_receiver_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()

                # Execute
                response = client.put(
                    self.endpoint.format(1), data=json.dumps({}), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_put_order_receiver_updated(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()
                order_receiver = self.create_order_receiver()
                data = {"first_name": "new_name"}

                # Execute
                response = client.put(
                    self.endpoint.format(order_receiver.get("id")), data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(str(resp_data["data"]["first_name"]), "new_name")

    def test_put_order_receiver_updated_self(self):
        with self.app() as client:
            with self.app_context():
                # Config
                user = self.set_session_key()
                order_receiver = self.create_order_receiver()
                data = {"user": "self"}

                # Execute
                response = client.put(
                    self.endpoint.format(order_receiver.get("id")), data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(str(resp_data["data"]["first_name"]), user.get("first_name"))

    def test_delete_order_receiver_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.delete(
                    self.endpoint.format("2"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_delete_order_receiver(self):
        with self.app() as client:
            with self.app_context():
                # Config
                user = self.set_session_key()
                order_receiver = self.create_order_receiver()

                # Execute
                response = client.delete(
                    self.endpoint.format(order_receiver.get("id")), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_delete_order_receiver_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Config
                user = self.set_session_key()

                # Execute
                response = client.delete(
                    self.endpoint.format("2"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)


class TestOrderReceiverCreateResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/order-receiver"

    def test_post_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(
                    self.endpoint, headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_order_receiver_already_settled(self):
        with self.app() as client:
            with self.app_context():

                self.set_session_key()
                self.create_order_receiver()

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps({}), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 409)

    def test_post_order_receiver_created_self(self):
        with self.app() as client:
            with self.app_context():
                # Config
                user = self.set_session_key()
                data = {"user": "self"}

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 201)
                self.assertEqual(str(resp_data["data"]["first_name"]), user.get("first_name"))

    def test_post_order_receiver_created(self):
        with self.app() as client:
            with self.app_context():
                # Config
                self.set_session_key()
                data = self.order_receiver_params

                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 201)
                self.assertEqual(str(resp_data["data"]["first_name"]), self.order_receiver_params.get("first_name"))
