import os
import unittest
import tensorflow

from entities.product import Product
from entities.furnish_type import FurnishType
from entities.product_type import ProductType
from machine_learning.price_prediction import PricePrediction


class PricePredictionUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pricePrediction = PricePrediction()
        cls.model_path = '../machine_learning/machinelearning'
        cls.product1 = Product(1, ProductType.Detached, FurnishType.Furnished, 1, 3, 60.1, 2000, 1, 3)
        cls.product2 = Product(2, ProductType.Detached, FurnishType.Furnished, 1, 3, 60.0, 2000, 2, 3)

    def test_if_model_path_exists_after_saving_it(self):
        if os.path.exists(self.model_path):
            os.remove(self.model_path)
        self.pricePrediction.make_model()
        self.assertTrue(os.path.exists(self.model_path))

    def test_if_load_model_returns_model(self):
        self.pricePrediction.make_model()
        self.assertTrue('Sequential' in str(type(self.pricePrediction.load_model())))

    def test_if_prediction_is_in_range(self):
        self.assertTrue(self.pricePrediction.make_prediction(self.product1) in range(45000, 70000))
        self.assertTrue(self.pricePrediction.make_prediction(self.product1) in range(45000, 70000))


if __name__ == '__main__':
    unittest.main()
