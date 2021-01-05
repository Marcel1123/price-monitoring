import uuid
import random
import timeit

from entities.product import Product

product_types = ['DETACHED', 'SEMI_DETACHED', 'NON_DETACHED', 'STUDIO', 'HOUSE', 'NULL']
furnish_types = ['FURNISHED', 'SEMI_FURNISHED', 'UNFURNISHED', 'NULL']
test_setup = """
from machine_learning.linear_regression import linear_regression
from tests.web_api_performance_testing import get_rand_product_for_api
"""


def get_rand_product_for_api():
    global product_types, furnish_types
    number_of_floors = random.randint(-1, 25)
    floor_number = random.randint(-1, number_of_floors)
    product = Product(id=uuid.uuid4(),
                      product_type=random.choice(product_types),
                      furnish_type=random.choice(furnish_types),
                      floor_number=floor_number,
                      number_of_floors=number_of_floors,
                      size=random.uniform(30.0, 300.0),
                      year_of_construction=random.randint(1980, 2025),
                      location_id="6c2f4e70-a6e4-4d30-87a6-4cfd046ce0ff",
                      number_of_rooms=random.randint(1, 10))
    return product


def test_api_speed_with_x_calls(x):
    time = timeit.timeit('linear_regression.estimate_price(get_rand_product_for_api())', setup=test_setup, number=x)
    print("Time taken for " + str(x) + " call(s): " + str(time))
    print("Average time taken: ", time/x)
    print()


def run_performance_tests():
    test_api_speed_with_x_calls(1)
    test_api_speed_with_x_calls(25)
    test_api_speed_with_x_calls(100)
    test_api_speed_with_x_calls(250)
    test_api_speed_with_x_calls(500)
    test_api_speed_with_x_calls(1000)
