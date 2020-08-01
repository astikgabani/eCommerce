from unittest import TestCase
from datetime import datetime, timedelta

from wsgi import app

from plugins.db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        with app.app_context():
            db.init_app(app)

        # Address
        cls.address_params = {
            "address_line_1": "223, Dummy Soc",
            "address_line_2": "Some Cross Road",
            "city": "Surat",
            "state": "Gujarat",
        }

        # cart
        cls.cart_params = {"total": 100}
        cls.cart_item_params = {"quantity": 5}
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
        cls.product_image_params = {"image_name": "test_image.png"}
        cls.product_category_params = {
            "name": "home_appliance",
            "value": "Home Appliance",
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
            "phone_no": "1111111111",
        }
        cls.user_confirmation_params = {
            "confirmed": False,
        }
        cls.user_session_params = {
            "ip": "10.0.0.1",
        }
        cls.user_session_token_params = {
            "refresh_token": "dummy_user_session",
        }
        cls.user_roles_params = {"role": "admin"}

    def setUp(self) -> None:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
        app.config["DEBUG"] = False
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # Make db empty
        with app.app_context():
            db.session.remove()
            db.drop_all()
