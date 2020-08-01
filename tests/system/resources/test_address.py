from tests.system.system_base_test import SystemBaseTest

import json


class TestAddressResource(SystemBaseTest):
    def setUp(self) -> None:
        super(TestAddressResource, self).setUp()
        self.endpoint = "/address"

    def test_get_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(self.endpoint)

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_get_list_of_address(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.get(self.endpoint, headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_post_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.post(
                    self.endpoint, data=json.dumps(self.address_params)
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_address_created(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.post(
                    self.endpoint,
                    data=json.dumps(self.address_params),
                    headers=self.headers,
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(resp_data["data"]["id"])

    def test_put_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.put(
                    self.endpoint, data=json.dumps(self.address_params)
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_put_address_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.put(
                    self.endpoint,
                    data=json.dumps(self.user_params),
                    headers=self.headers,
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_put_address_updated(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()
                response = client.post(
                    self.endpoint,
                    data=json.dumps(self.address_params),
                    headers=self.headers,
                )
                data = json.loads(response.data).get("data")
                data.update({"city": "updated_city"})

                # Execute
                response = client.put(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(resp_data["data"]["city"], "updated_city")

    def test_delete_unauthorized(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.delete(
                    self.endpoint, data=json.dumps(self.address_params)
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_delete_address_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()
                data = {"id": "10"}

                # Execute
                response = client.delete(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_delete_address_updated(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()
                response = client.post(
                    self.endpoint,
                    data=json.dumps(self.address_params),
                    headers=self.headers,
                )
                data = {"id": json.loads(response.data).get("data").get("id")}

                # Execute
                response = client.delete(
                    self.endpoint, data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 200)
