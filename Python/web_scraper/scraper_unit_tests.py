import unittest
import os
from web_scraper import scraper


class ScrapperUnitTests(unittest.TestCase):
    scraper_from_tutorial_export_path = None
    static_scraper_export_path = None

    @classmethod
    def setUpClass(cls):
        cls.scraper_from_tutorial_export_path = '../../Data/tutorial_results.csv'
        cls.static_scraper_export_path = '../../Data/static_results.csv'
        cls.scraper_from_tutorial_result = scraper.scraper_from_tutorial(cls.scraper_from_tutorial_export_path)
        cls.static_scraper_result = scraper.static_scraper(cls.static_scraper_export_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.scraper_from_tutorial_export_path):
            os.remove(cls.scraper_from_tutorial_export_path)
        if os.path.exists(cls.static_scraper_export_path):
            os.remove(cls.static_scraper_export_path)

    def test_if_scraper_from_tutorial_returns_not_none(self):
        self.assertTrue(self.scraper_from_tutorial_result is not None)

    def test_if_scraper_from_tutorial_returns_list(self):
        self.assertTrue(isinstance(self.scraper_from_tutorial_result, list))

    def test_if_scraper_from_tutorial_returned_list_has_dictionaries(self):
        if self.static_scraper_result is not None:
            self.assertTrue(isinstance(self.scraper_from_tutorial_result[0], dict))
        else:
            self.fail('Scraper from tutorial result is None')

    def test_if_scraper_from_tutorial_export_file_was_created(self):
        flag = False
        if os.path.exists(self.scraper_from_tutorial_export_path):
            flag = True
        self.assertTrue(flag)

    def test_if_static_scraper_returns_not_none(self):
        self.assertTrue(self.static_scraper_result is not None)

    def test_if_static_scraper_returns_list(self):
        self.assertTrue(isinstance(self.static_scraper_result, list))

    def test_if_static_scraper_returned_list_has_dictionaries(self):
        if self.static_scraper_result is not None:
            self.assertTrue(isinstance(self.static_scraper_result[0], dict))
        else:
            self.fail('Static scraper result is None')

    def test_if_static_scraper_export_file_was_created(self):
        flag = False
        if os.path.exists(self.static_scraper_export_path):
            flag = True
        self.assertTrue(flag)

    def test_if_static_scraper_returned_list_has_117_elements(self):
        self.assertEqual(len(self.static_scraper_result), 117)

    def test_if_static_scraper_has_correct_first_result(self):
        price = '$295.99'
        title = 'Asus VivoBook X4...'
        description = 'Asus VivoBook X441NA-GA190 Chocolate Black, 14", Celeron N3450, 4GB, 128GB SSD, Endless OS, ENG kbd'
        reviews = '14 reviews'
        self.assertEqual(self.static_scraper_result[0]['price'], price)
        self.assertEqual(self.static_scraper_result[0]['title'], title)
        self.assertEqual(self.static_scraper_result[0]['description'], description)
        self.assertEqual(self.static_scraper_result[0]['reviews'], reviews)


if __name__ == '__main__':
    unittest.main()
