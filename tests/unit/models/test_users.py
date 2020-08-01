from unittest.mock import MagicMock, PropertyMock, patch

from tests.unit.unit_base_test import UnitBaseTest

import models.users

from datetime import datetime
from time import time


class TestUserModel(UnitBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "email": "temp@test.com",
            "password": "password",
            "first_name": "Astik",
            "last_name": "Gabani",
            "phone_no": 9999999999,
            "gender": models.users.GenderEnum.male,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.users.UserModel(**self.params)

    def test_pre_save(self):
        # Configure
        mock_pwd_check = self.obj.check_password_already_hashed = MagicMock()
        mock_pwd_check.return_value = False
        mock_pwd_hash = self.obj.get_password_hash = MagicMock()
        mock_pwd_hash.return_value = "hashed-pwd"

        # Execute
        self.obj.pre_save()

        # Assert
        self.assertEqual(self.obj.password, "hashed-pwd")
        mock_pwd_check.assert_called_once_with()
        mock_pwd_hash.assert_called_once_with("password")

    def test_pre_save_already_hashed(self):
        # Configure
        mock_pwd_check = self.obj.check_password_already_hashed = MagicMock()
        mock_pwd_check.return_value = True
        mock_pwd_hash = self.obj.get_password_hash = MagicMock()
        mock_pwd_hash.return_value = "hashed-pwd"

        # Execute
        self.obj.pre_save()

        # Assert
        self.assertEqual(self.obj.password, "password")
        mock_pwd_check.assert_called_once_with()
        assert not mock_pwd_hash.called

    def test_get_password_hash(self):
        # Configure
        mock_generate_hash = models.users.generate_password_hash = MagicMock()
        mock_generate_hash.return_value = "hashed-pwd"

        # Execute
        output = self.obj.get_password_hash("pwd")

        # Assert
        self.assertEqual(output, "hashed-pwd")
        mock_generate_hash.assert_called_once_with("pwd")

    @patch("models.users.UserModel.most_recent_confirmation", new_callable=PropertyMock)
    def test_send_confirmation_email(self, mock_recent_confirm):
        # Configure
        mock_confirmation_mail = models.users.send_confirmation_mail = MagicMock()
        mock_request = models.users.request = MagicMock()
        mock_request.url_root = "https://www.temp.com/"
        mock_recent_confirm.return_value.id = 1
        mock_url_for = models.users.url_for = MagicMock()
        mock_url_for.return_value = "/confirm/1"
        link = "https://www.temp.com/confirm/1"

        # Execute
        self.obj.send_confirmation_email()

        # Assert
        mock_confirmation_mail.assert_called_once_with(self.obj.email, link)
        mock_url_for.assert_called_once_with("useremailconfirm", confirmation_id=1)

    def test_verify_password(self):
        # Configure
        mock_check_hash = models.users.check_password_hash = MagicMock()
        mock_check_hash.return_value = True

        # Execute
        output = self.obj.verify_password("pwd")

        # Assert
        self.assertEqual(
            output, True, "verify_password, password is not checking properly"
        )
        mock_check_hash.assert_called_once_with(self.obj.password, "pwd")

    def test_check_password_already_hashed(self):
        # Configure
        self.obj.password = "pbkdf2:sha256:dummy_password"

        # Execute
        output = self.obj.check_password_already_hashed()

        # Assert
        self.assertEqual(
            output,
            True,
            "check_password_already_hashed, Password hash is not checking properly",
        )

    def test_check_password_already_hashed_false(self):
        # Configure
        self.obj.password = "dummy_password"

        # Execute
        output = self.obj.check_password_already_hashed()

        # Assert
        self.assertEqual(
            output,
            False,
            "check_password_already_hashed, Password hash is not checking properly",
        )


class TestUserConfirmationModel(UnitBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "expire_at": 121212,
            "confirmed": True,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.users.UserConfirmationModel(**self.params)

    def test_pre_save(self):
        # Configure
        self.obj.id = None

        # Execute
        self.obj.pre_save()

        # Assert
        self.assertIsNotNone(self.obj.id)
        self.assertAlmostEqual(
            time() + models.users.CONFIRMATION_EXPIRATION_DELTA,
            self.obj.expire_at,
            delta=5,
        )

    def test_expired(self):
        # Configure
        self.obj.expire_at = time() - 5

        # Execute
        output = self.obj.expired

        # Assert
        self.assertEqual(output, True)

    def test_expired_active(self):
        # Configure
        self.obj.expire_at = time() + 100

        # Execute
        output = self.obj.expired

        # Assert
        self.assertEqual(output, False)

    def test_force_to_expire(self):
        # Configure
        mock_expired = models.users.UserConfirmationModel.expired = PropertyMock()
        mock_expired.return_value = False
        self.obj.expire_at = 100
        mock_save = self.obj.save_to_db = MagicMock()

        # Execute
        self.obj.force_to_expire()

        # Assert
        mock_save.assert_called_once_with()
        self.assertNotEqual(self.obj.expire_at, 100)
        self.assertAlmostEqual(self.obj.expire_at, int(time()), delta=3)

    def test_force_to_expire_already_expired(self):
        # Configure
        mock_expired = models.users.UserConfirmationModel.expired = PropertyMock()
        mock_expired.return_value = True
        self.obj.expire_at = 100
        mock_save = self.obj.save_to_db = MagicMock()

        # Execute
        self.obj.force_to_expire()

        # Assert
        assert not mock_save.called
        self.assertEqual(self.obj.expire_at, 100)
        self.assertNotAlmostEqual(self.obj.expire_at, int(time()), delta=3)
