from tests.integration.integration_base_test import IntegrationBaseTest

from models.products import ProductModel, ProductAttributeModel, ProductAttributeOptionsModel, ProductImageModel
from models.product_category import ProductCategoryModel


class TestProductModel(IntegrationBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.model = ProductModel
        self.params = self.product_params
        with self.app_context():
            category = ProductCategoryModel(**self.product_category_params)
            category.save_to_db()

            self.params.update({"category_id": category.id})

        self.test_passing_param = {
            "name": self.product_params.get("name")
        }
        self.test_failing_param = {
            "name": "dummy_product"
        }

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_category_relationship(self):
        with self.app_context():
            product = ProductModel(**self.params)
            product.save_to_db()

            self.assertEqual(product.category.name, self.product_category_params.get("name"))


class TestProductAttributeModel(IntegrationBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.model = ProductAttributeModel
        self.params = self.product_attr_params
        with self.app_context():
            product = ProductModel(**self.product_params)
            product.save_to_db()

            self.params.update({"product_id": product.id})

        self.test_passing_param = {
            "name": self.product_attr_params.get("name")
        }
        self.test_failing_param = {
            "name": "dummy_product"
        }

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_product_relationship(self):
        with self.app_context():
            product_attr = ProductAttributeModel(**self.params)
            product_attr.save_to_db()

            self.assertEqual(product_attr.product.name, self.product_params.get("name"))


class TestProductAttributeOptionsModel(IntegrationBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.model = ProductAttributeOptionsModel
        self.params = self.product_attr_options_params
        with self.app_context():
            product_attr = ProductAttributeModel(**self.product_attr_params)
            product_attr.save_to_db()

            self.params.update({"attr_id": product_attr.id})

        self.test_passing_param = {
            "name": self.product_attr_options_params.get("name")
        }
        self.test_failing_param = {
            "name": "dummy_product"
        }

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_product_relationship(self):
        with self.app_context():
            product_attr_opt = ProductAttributeOptionsModel(**self.params)
            product_attr_opt.save_to_db()

            self.assertEqual(product_attr_opt.attr.name, self.product_attr_params.get("name"))


class TestProductImage(IntegrationBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.model = ProductImageModel
        self.params = self.product_image_params
        self.test_passing_param = {
            "image_name": self.product_image_params.get("image_name")
        }
        self.test_failing_param = {
            "image_name": "dummy_product"
        }

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()