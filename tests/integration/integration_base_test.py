from tests.base_test import BaseTest


class IntegrationBaseTest(BaseTest):
    def super_model_methods_testing(self):
        with self.app_context():
            item = self.model(**self.params)
            item.save_to_db()

            # get_active() & save_to_db() method
            self.assertIsNotNone(self.model.get_active().first())

            # get_query() method
            self.assertIsNotNone(
                self.model.get_query(**self.test_passing_param).first()
            )
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
            self.assertIsNone(self.model.get_item(id=item.id))
