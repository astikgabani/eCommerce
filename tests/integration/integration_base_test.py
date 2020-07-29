from unittest import TestCase
from datetime import datetime, timedelta

from models.helper.enums import *

from wsgi import app

from plugins.db import db


class IntegrationBaseTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Address
        cls.address_params = {
            "type": AddressTypeEnum.shipping,
            "address_line_1": "223, Dummy Soc",
            "address_line_2": "Some Cross Road",
            "city": "Surat",
            "state": "Gujarat"
        }

        # cart
        cls.cart_params = {
            "total": 100
        }
        cls.cart_item_params = {
            "quantity": 5
        }
        cls.coupon_params = {
            "code": "TEST20",
            "value": 20,
            "max_value": 75,
            "start": datetime.utcnow() - timedelta(days=5),
            "expire": datetime.utcnow() + timedelta(days=5),
        }

        # Order
        cls.order_params = {
            "shipping_cost": 20.00,
            "total": 50,
        }
        cls.order_receiver_params = {
            "first_name": "Astik",
            "last_name": "Gabani",
            "phone_no": 9999559955,
        }

        # product
        cls.product_params = {
            "name": "product",
            "description": "this is the awesome product",
            "slug": "temp-slug",
            "price": 70,
        }
        cls.product_attr_params = {
            "name": "color",
            "value": "Color",
        }
        cls.product_attr_options_params = {
            "name": "Color",
            "value": "color",
            "price_change": 5,
        }
        cls.product_review_params = {
            "ratings": 3,
            "comments": "Comments",
        }

        # User
        cls.user_params = {
            "email": "testing@email.com",
            "password": "test@123",
            "first_name": "test",
            "last_name": "last",
            "phone_no": 1111111111
        }
        cls.user_confirmation_params = {
            "expire_at": 121212,
            "confirmed": True,
        }
        cls.user_session_params = {
            "ip": "10.0.0.1",
        }
        cls.user_session_token_params = {
            "refresh_token": "dummy_user_session",
        }
        cls.user_roles_params = {
            "role": "admin"
        }

    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"
        with app.app_context():
            db.init_app(app)
            db.create_all()
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Make db empty
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def super_model_methods_testing(self):
        with self.app_context():
            item = self.model(**self.params)
            item.save_to_db()

            # get_active() & save_to_db() method
            self.assertIsNotNone(self.model.get_active().first())

            # get_query() method
            self.assertIsNotNone(self.model.get_query(**self.test_passing_param).first())
            self.assertIsNone(self.model.get_query(**self.test_failing_param).first())

            # get_item() method
            self.assertIsNotNone(self.model.get_item(**self.test_passing_param))
            self.assertIsNone(self.model.get_item(**self.test_failing_param))

            # get_items() method
            self.assertEqual(self.model.get_items(**self.test_passing_param), [item])
            self.assertEqual(self.model.get_items(**self.test_failing_param), [])

            # deactivate() method
            item.deactivate()
            self.assertEqual(item.active, False)
            self.assertIsNone(self.model.get_active().first())
