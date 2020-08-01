from tests.unit.unit_base_test import UnitBaseTest

import models.review


class TestOrderModel(UnitBaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.params = {
            "id": 1,
            "ratings": 3,
            "comments": "Comments",
        }
        self.obj = models.review.ReviewModel(**self.params)

    def test_pre_save(self):
        # Execute
        self.obj.pre_save()
