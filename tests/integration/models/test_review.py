from tests.integration.integration_base_test import IntegrationBaseTest

from models.review import ReviewModel
from models.products import ProductModel
from models.users import UserModel


class TestReviewModel(IntegrationBaseTest):

    def setUp(self) -> None:
        super().setUp()
        self.model = ReviewModel
        self.params = self.product_review_params
        with self.app_context():
            product = ProductModel(**self.product_params)
            product.save_to_db()

            user = UserModel(**self.user_params)
            user.save_to_db()

            self.params.update({"product_id": product.id, "user_id": user.id})

        self.test_passing_param = {
            "comments": self.product_review_params.get("comments")
        }
        self.test_failing_param = {
            "comments": "Temp Name"
        }

    def test_super_model_methods_testing(self):
        self.super_model_methods_testing()

    def test_self_reference_relationship(self):
        with self.app_context():
            review = ReviewModel(**self.params)
            review.save_to_db()

            self.assertEqual(review.product.name, self.product_params.get("name"))
            self.assertEqual(review.user.email, self.user_params.get("email"))
