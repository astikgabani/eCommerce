from tests.integration.integration_base_test import IntegrationBaseTest

from models.product_category import ProductCategoryModel


class TestProductCategoryModel(IntegrationBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.model = ProductCategoryModel
        self.params = self.product_category_params
        with self.app_context():
            parent_data = {"name": "parent_data", "value": "Parent Category"}
            parent = ProductCategoryModel(**parent_data)
            parent.save_to_db()
            self.params.update({"parent_id": parent.id})

        self.test_passing_param = {"name": self.product_category_params.get("name")}
        self.test_failing_param = {"name": "dummy Name"}

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_self_reference_relationship(self):
        with self.app_context():
            category = ProductCategoryModel(**self.params)
            category.save_to_db()

            self.assertEqual(category.parent_rel.name, "parent_data")
