from tests.integration.integration_base_test import IntegrationBaseTest

from models.address import AddressModel, AddressTypeEnum
from models.users import UserModel


class TestAddressModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = AddressModel
        self.test_passing_param = {"city": "Surat"}
        self.test_failing_param = {"city": "Mumbai"}
        self.params = self.address_params

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_user_relationship(self):
        with self.app_context():
            user = UserModel(**self.user_params)
            user.save_to_db()

            address = AddressModel(user_id=user.id, **self.params)
            address.save_to_db()

            self.assertEqual(address.user.email, self.user_params.get("email"))
