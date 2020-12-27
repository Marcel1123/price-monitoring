import uvicorn

from machine_learning.data_preparation.data_preparation import DataPreparation
from web_scraper.real_estates import *

if __name__ == '__main__':
    # DataPreparation()
    uvicorn.run("web_api.new_product_prediction:app")
