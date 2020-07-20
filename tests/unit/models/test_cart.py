from unittest.mock import MagicMock, patch, PropertyMock

from tests.unit.unit_base_test import UnitBaseTest

import models.cart

from datetime import datetime


class TestCartModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.cart_params = {
            "id": 1,
            "total": 10.00,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
            "user_id": 1,
            "session_id": 1,
            "coupon_id": 1
            }
        self.cart_obj = models.cart.CartModel(**self.cart_params)

    @patch("models.cart.CartModel.count_total", new_callable=PropertyMock)
    def test_pre_save(self, count_total_mock):
        # Configure
        count_total_mock.return_value = 20

        # Execute
        self.cart_obj.pre_save()

        # Assert
        self.assertEqual(self.cart_obj.total, 20, "pre_save, total is not updating.")

    def test_count_total(self):
        # Configure
        [mock_cart_item] = self.cart_obj.cart_items = [MagicMock()]
        mock_cart_item.get_price.return_value = 20
        mock_coupon = self.cart_obj.coupon = MagicMock()
        mock_cart_item.product.coupons = [mock_coupon]
        mock_coupon.get_discount_price.return_value = 3

        # Execute
        output = self.cart_obj.count_total

        # Assert
        self.assertEqual(output, 17, "count_total, total is not calculating correctly.")
        mock_coupon.get_discount_price.assert_called_once_with(20)
        mock_cart_item.get_price.assert_called_once_with()

    def test_count_total_coupon_not_exist(self):
        # Configure
        [mock_cart_item] = self.cart_obj.cart_items = [MagicMock()]
        mock_cart_item.get_price.return_value = 20
        mock_coupon = self.cart_obj.coupon = MagicMock()
        mock_cart_item.product.coupons = [MagicMock()]
        mock_coupon.get_discount_price.return_value = 3

        # Execute
        output = self.cart_obj.count_total

        # Assert
        self.assertEqual(output, 20, "count_total, total is not calculating correctly.")
        assert not mock_coupon.get_discount_price.called
        mock_cart_item.get_price.assert_called_once_with()

    def test_get_or_create_existing_cart(self):
        # Configure
        mock_get_item = models.cart.CartModel.get_item = MagicMock()
        mock_get_item.return_value = self

        # Execute
        output = models.cart.CartModel.get_or_create(id=10, total=50)

        # Assert
        mock_get_item.assert_called_once_with(id=10, total=50)
        self.assertEqual(output, self, "get_or_create, Not returning the existing cart.")

    def test_get_or_create_new_cart_creation(self):
        # Configure
        mock_get_item = models.cart.CartModel.get_item = MagicMock()
        mock_get_item.return_value = None
        mock_save_to_db = models.cart.CartModel.save_to_db = MagicMock()

        # Execute
        output = models.cart.CartModel.get_or_create(id=10, total=50)

        # Assert
        mock_get_item.assert_called_once_with(id=10, total=50)
        mock_save_to_db.assert_called_once_with()
        self.assertIsInstance(output, self.cart_obj.__class__, "get_or_create, Newly created object is not an instance of CartModel.")
        self.assertEqual(output.id, 10, "get_or_create, Not creating new cart with the given id value.")
        self.assertEqual(output.total, 50, "get_or_create, Not creating new cart with the given total value.")
        self.assertNotEqual(output, self, "get_or_create, Not creating new cart.")


class TestCartItemModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.cart_params = {
            "id": 1,
            "quantity": 5,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
            "cart_id": 1,
            "product_id": 1,
            "attr_option_id": 1
            }
        self.cart_obj = models.cart.CartItemsModel(**self.cart_params)

    def test_pre_save(self):
        # Configure
        mock_product = self.cart_obj.product = MagicMock()
        [mock_attr] = mock_product.attrs = [MagicMock()]
        [mock_attr_option] = mock_attr.attrs_options = [MagicMock()]

        # Execute
        self.cart_obj.pre_save()

        # Assert
        # Assertions are handle in pre_save method it self

    def test_get_price(self):
        # Configure
        mock_product = self.cart_obj.product = MagicMock()
        mock_product.price = 100
        mock_attr_option = self.cart_obj.product_option = MagicMock()
        mock_attr_option.price_change = 9

        # Execute
        output = self.cart_obj.get_price()

        # Assert
        self.assertEqual(output, 109, "get_price, Price change of product attribute option is not working properly")

    def test_post_save(self):
        # Configure
        mock_count_total = self.cart_obj.cart = MagicMock()
        mock_count_total.count_total = 20

        # Execute
        self.cart_obj.post_save()

        # Assert
        self.assertEqual(self.cart_obj.cart.total, 20, "post_save, count total is not working.")
