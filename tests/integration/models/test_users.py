from tests.integration.integration_base_test import IntegrationBaseTest

from models.users import (
    UserModel,
    UserSessionModel,
    UserSessionTokenModel,
    UserRoleModel,
    UserConfirmationModel,
)


class TestUserModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserModel
        self.params = self.user_params
        self.test_passing_param = {"email": self.user_params.get("email")}
        self.test_failing_param = {"email": "Temp Name"}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()


class TestUserSessionModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserSessionModel
        self.params = self.user_session_params
        with self.app_context():
            user = UserModel(**self.user_params)
            user.save_to_db()

            self.params.update({"user_id": user.id})

        self.test_passing_param = {"ip": self.user_session_params.get("ip")}
        self.test_failing_param = {"ip": "0.0.0.0"}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_self_reference_relationship(self):
        with self.app_context():
            session = UserSessionModel(**self.params)
            session.save_to_db()

            self.assertEqual(session.user.email, self.user_params.get("email"))


class TestUserSessionTokenModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserSessionTokenModel
        self.params = self.user_session_token_params
        with self.app_context():
            session = UserSessionModel(**self.user_session_params)
            session.save_to_db()

            self.params.update({"session_id": session.id})

        self.test_passing_param = {
            "refresh_token": self.user_session_token_params.get("refresh_token")
        }
        self.test_failing_param = {"refresh_token": "dummy_tokens"}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_self_reference_relationship(self):
        with self.app_context():
            token = UserSessionTokenModel(**self.params)
            token.save_to_db()

            self.assertEqual(token.session.ip, self.user_session_params.get("ip"))


class TestUserRoleModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserRoleModel
        self.params = self.user_roles_params
        self.test_passing_param = {"role": self.user_roles_params.get("role")}
        self.test_failing_param = {"role": "dummy_role"}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()


class TestUserConfirmationModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserConfirmationModel
        self.params = self.user_confirmation_params
        with self.app_context():
            user = UserModel(**self.user_params)
            user.save_to_db()

            self.params.update({"user_id": user.id})

        self.test_passing_param = {
            "confirmed": self.user_confirmation_params.get("confirmed")
        }
        self.test_failing_param = {"confirmed": True}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_self_reference_relationship(self):
        with self.app_context():
            confirmation = UserConfirmationModel(**self.params)
            confirmation.save_to_db()

            self.assertEqual(confirmation.user.email, self.user_params.get("email"))
