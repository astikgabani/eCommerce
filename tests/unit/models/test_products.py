from unittest.mock import MagicMock, PropertyMock, patch

from tests.unit.unit_base_test import UnitBaseTest

import models.products

from datetime import datetime


class TestProductModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "name": "product",
            "description": "this is the awesome product",
            "slug": "temp-slug",
            "price": 70,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.products.ProductModel(**self.params)

    def test_pre_save(self):
        # Configure
        self.obj.slug = "old-slug"
        mock_slug_generator = models.helper.utils.unique_slug_generator = MagicMock()
        mock_slug_generator.return_value = "new-slug"

        # Execute
        self.obj.pre_save()

        # Assert
        self.assertEqual(self.obj.slug, "old-slug")
        assert not mock_slug_generator.called

    def test_pre_save_slug_not_present(self):
        # Configure
        self.obj.slug = None
        mock_slug_generator = models.products.unique_slug_generator = MagicMock()
        mock_slug_generator.return_value = "new-slug"

        # Execute
        self.obj.pre_save()

        # Assert
        self.assertEqual(self.obj.slug, "new-slug")
        mock_slug_generator.assert_called_once_with(self.obj)


class TestProductAttributeOptionsModel(UnitBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "name": "Color",
            "value": "color",
            "price_change": 5,
            "active": True,
            "created": datetime.utcnow(),
            "updated": datetime.utcnow(),
        }
        self.obj = models.products.ProductAttributeOptionsModel(**self.params)

    def test_pre_save(self):
        # Execute
        self.obj.pre_save()
