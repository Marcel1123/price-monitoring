import unittest

from entities.product import Product
from entities.furnish_type import FurnishType
from entities.product_type import ProductType
from machine_learning.data_preparation.identical_products import IdenticalProducts


class IdenticalProductsUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.identicalProducts = IdenticalProducts()
        cls.product1 = Product(1, ProductType.Detached, FurnishType.Furnished, 1, 3, 60.1, 2000, 1, 3)
        cls.product2 = Product(2, ProductType.Detached, FurnishType.Furnished, 1, 3, 60.0, 2000, 2, 3)
        cls.product3 = Product(3, ProductType.Detached, FurnishType.Furnished, 1, 6, 60.0, 1980, 3, 3)
        cls.product4 = Product(4, ProductType.Semi_detached, FurnishType.Furnished, 0, 8, 60.0, 1900, 4, 3)
        cls.product5 = Product(5, ProductType.Semi_detached, FurnishType.Furnished, -1, 3, 30.0, 2020, 5, 1)
        cls.product6 = Product(6, ProductType.Semi_detached, FurnishType.Furnished, 1, 5, 50.0, 2000, 6, 2)
        cls.product7 = Product(7, ProductType.Semi_detached, FurnishType.Furnished, 6, 6, 30.0, 2000, 7, 1)
        cls.products = [cls.product3, cls.product4, cls.product5, cls.product6, cls.product7]

    def test_if_identical_products_returns_not_none(self):
        self.assertTrue(self.identicalProducts is not None)

    def test_if_products_not_none(self):
        self.assertTrue(self.product1 is not None)
        self.assertTrue(self.product2 is not None)
        self.assertTrue(self.product3 is not None)

    def test_if_compare_products_returns_boolean(self):
        self.assertTrue(isinstance(self.identicalProducts.compare(self.product1, self.product2), bool))

    def test_if_compare_same_product_returns_true(self):
        self.assertTrue(self.identicalProducts.compare(self.product1, self.product1) is True)

    def test_if_compare_similar_products_returns_true(self):
        self.assertTrue(self.identicalProducts.compare(self.product1, self.product2) is True)

    def test_if_compare_different_products_returns_false(self):
        for i in range(0, len(self.products)):
            for j in range(i + 1, len(self.products)):
                self.assertTrue(self.identicalProducts.compare(self.products[i], self.products[j]) is False)


if __name__ == '__main__':
    unittest.main()
