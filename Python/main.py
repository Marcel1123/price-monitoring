import uvicorn

from machine_learning.data_preparation.data_preparation import DataPreparation
from tests.web_api_performance_testing import run_performance_tests

from web_scraper.real_estates import *


if __name__ == '__main__':
    # DataPreparation()
    uvicorn.run("web_api.new_product_prediction:app")
    # run_performance_tests()
