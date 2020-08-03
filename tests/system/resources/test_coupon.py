from tests.system.system_base_test import SystemBaseTest

from datetime import datetime, timedelta

import json


class TestCouponResource(SystemBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/coupon/{}"

    def get_config_data(self):
        data = self.coupon_params.copy()
        data.pop("code", "")
        data.update({
            "start": (datetime.utcnow() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S"),
            "expire": (datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")
        })
        return data

    def test_get_detail_coupon(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                coupon = self.create_coupon()

                # Execute
                response = client.get(self.endpoint.format(coupon.get("code")), headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Execute
                response = client.get(self.endpoint.format("something"), headers=self.headers)

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_post_coupon_already_created(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()
                coupon = self.create_coupon()
                data = self.get_config_data()

                # Execute
                response = client.post(
                    self.endpoint.format(coupon.get("code")), data=json.dumps(data), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 409)

    def test_post_admin_access_required(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.post(
                    self.endpoint.format("code"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_post_coupon_created(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()
                data = self.get_config_data()

                # Execute
                response = client.post(
                    self.endpoint.format("NEW40"), data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 201)
                self.assertEqual(resp_data["data"]["code"], "NEW40")
                self.assertIsNotNone(resp_data["data"]["id"])

    def test_put_admin_access_required(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.put(
                    self.endpoint.format("code"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_put_coupon_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()

                # Execute
                response = client.put(
                    self.endpoint.format("NEW40"), data=json.dumps({}), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)

    def test_put_coupon_created(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()
                data = self.get_config_data()
                client.post(
                    self.endpoint.format("NEW40"), data=json.dumps(data), headers=self.headers
                )
                data.update({"max_value": 200})

                # Execute
                response = client.put(
                    self.endpoint.format("NEW40"), data=json.dumps(data), headers=self.headers
                )
                resp_data = json.loads(response.data)

                # Assert
                self.assertEqual(response.status_code, 200)
                self.assertEqual(resp_data["data"]["max_value"], 200)
                self.assertIsNotNone(resp_data["data"]["id"])

    def test_delete_coupon_deleted(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()
                data = self.get_config_data()
                client.post(
                    self.endpoint.format("NEW40"), data=json.dumps(data), headers=self.headers
                )

                # Execute
                response = client.delete(
                    self.endpoint.format("NEW40"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 200)

    def test_delete_admin_access_required(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.set_session_key()

                # Execute
                response = client.delete(
                    self.endpoint.format("code"), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 401)

    def test_delete_coupon_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Configure
                self.get_admin_account()

                # Execute
                response = client.delete(
                    self.endpoint.format("NEW40"), data=json.dumps({}), headers=self.headers
                )

                # Assert
                self.assertEqual(response.status_code, 404)
