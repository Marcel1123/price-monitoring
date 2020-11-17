# clean data (remove duplicates, correct errors, deal with missing values, normalization, data type conversions)

# randomize data

# visualize data to detect relevant relationships between variables or class imbalances

# split into training + validation + test
from numpy import nan

from entities.city import City
from entities.furnish_type import FurnishType
from entities.location import Location
from entities.product import Product
from entities.product_history import ProductHistory
import datetime
import re

from entities.product_type import ProductType
from machine_learning.data_preparation import analyse_data


def float_or_na(value):
    return float(value if value != 'N/A' else 'nan')


def get_date(line):
    scrap_date = "15.11.2020"
    product_date = line[-11]
    if 'azi' in product_date.lower():
        date_time_obj = datetime.datetime.strptime(scrap_date, '%d.%m.%Y')
    elif 'ieri' in product_date.lower():
        date_time_obj = datetime.datetime.strptime(scrap_date, '%d.%m.%Y') - datetime.timedelta(1)
    else:
        date_time_obj = datetime.datetime.strptime(product_date[-10:], '%d.%m.%Y')
    return date_time_obj


def get_year(line):
    number = re.findall(r'\d+', line[-1])
    if number:
        return number[0]
    return nan


def get_size(line):
    number = re.findall(r'\d+', line[10])
    if number:
        return number[0]
    else:
        number = re.findall(r'\d+\.\d+', line[10])
        if number:
            return number[0]
    return nan


def get_floor_number(line):
    number = line[9]
    if number.lower() in "parter":
        return "0"
    if number.lower() in "demisol":
        return "-1"
    return number


def get_product_type(line):
    my_type = line[5]
    for existing_type in ProductType:
        if my_type == str(existing_type).split(".")[-1]:
            return existing_type
    return ""


def get_furnish_type(line):
    my_type = line[6]
    for existing_type in FurnishType:
        if my_type == str(existing_type).split(".")[-1]:
            return existing_type
    return ""


class DataPreparation:
    city = City("c_1", "Iasi", "Romania")

    def __init__(self):
        print("Data preparation...")
        url_csv_scrapped = "D:\Projects\ASET\price-monitoring\Data\imobiliare_ro_apartamente_iasi_15-11-2020_new_size.csv"
        url_new = "D:\Projects\ASET\price-monitoring\Data\db.csv"

        with open(url_csv_scrapped, "r") as fs, open(url_new, "w") as fn:
            print(fs.readline().replace("\n", "").split(","))
            line = fs.readline().replace("\n", "")

            products = []
            features_columns = ["size", "location", "year", "rooms", "type", "furnish", "floor", "total_floors",
                                "price"]

            while line:
                product, history, location = self.process_line_for_db(line.split(","))
                features = self.process_for_machine_learning(product, history, location)
                if features:
                    products.append(features)
                line = fs.readline().replace("\n", "")
            print("total products with price: ", len(products))
            analyse_data.check_relevant_features(features_columns, products)

    def process_for_machine_learning(self, product, history, location):
        # eliminate data that don't provide information
        if 'N/A' in history.price or nan == history.price:
            return None
        features = [float_or_na(product.size),
                    int(product.location_id[-1]),
                    float_or_na(product.year_of_construction),
                    float_or_na(product.number_of_rooms),
                    product.product_type.value,
                    product.furnish_type.value,
                    float_or_na(product.floor_number),
                    float_or_na(product.number_of_floors),
                    float_or_na(history.price)]
        return features

    def process_line_for_db(self, line):
        location_id = "l_1"
        history_id = "h_1"
        product_id = "p_1"

        location = Location(id=location_id,
                            city_id=self.city.id,
                            address=line[4])
        history = ProductHistory(id=history_id,
                                 product_id=product_id,
                                 date=get_date(line),
                                 price=line[2],
                                 currency_type="EUR")
        product = Product(id=product_id,
                          product_type=get_product_type(line),
                          furnish_type=get_furnish_type(line),
                          floor_number=get_floor_number(line),
                          number_of_floors=line[9],
                          size=get_size(line),
                          year_of_construction=get_year(line),
                          location_id=location_id,
                          number_of_rooms=line[7])
        return product, history, location
