# clean data (remove duplicates, correct errors, deal with missing values, normalization, data type conversions)

# randomize data

# visualize data to detect relevant relationships between variables or class imbalances

# split into training + validation + test
from numpy import nan
from entities.city import City
from entities.location import Location
from entities.product import Product
from entities.product_history import ProductHistory
from entities.furnish_type import FurnishType
from entities.product_type import ProductType
from machine_learning.data_preparation import analyse_data
import datetime
import re
import uuid
import unidecode

url_csv_scrapped = "..\\Data\\estates.csv"
date_different = 1

city = City(uuid.uuid4(), "Iasi", "Romania")
locations = dict()  # address - key ; uuid address - value
products = []
history_list = []


def float_or_na(value):
    return float(value if value != 'N/A' else 'nan')


def get_date(line):
    product_date = line[-11]
    try:
        scrap_date = str(datetime.datetime.strptime(line[0], '%d.%m.%Y')[:-9])
    except ValueError:
        try:
            scrap_date = str(datetime.datetime.strptime(line[0].replace('"', ""), '%B %d %Y'))[:-9]
        except ValueError:
            scrap_date = str(datetime.datetime.strptime(line[0].replace('"', ""), '%d-%b-%y'))[:-9]

    if 'azi' in product_date.lower():
        try:
            date_time_obj = datetime.datetime.strptime(scrap_date, '%d.%m.%Y')
        except ValueError:
            date_time_obj = datetime.datetime.strptime(scrap_date, '%Y-%m-%d') - datetime.timedelta(1)
    elif 'ieri' in product_date.lower():
        try:
            date_time_obj = datetime.datetime.strptime(scrap_date, '%d.%m.%Y') - datetime.timedelta(1)
        except ValueError:
            date_time_obj = datetime.datetime.strptime(scrap_date, '%Y-%m-%d') - datetime.timedelta(1)
    else:
        date_time_obj = datetime.datetime.strptime(product_date[-10:], '%d.%m.%Y')
    return date_time_obj


def get_year(line):
    # get first year
    number = re.findall(r'\d+', line[-1])
    if number:
        return number[0]
    return "NULL"


def get_size(line):
    number = re.findall(r'\d+\.\d+', line[10])
    if number:
        return number[0]
    else:
        number = re.findall(r'\d+', line[10])
        if number:
            return number[0]
    return "NULL"


def get_floor_number(line):
    number = line[9]
    if number.lower() in "parter":
        return "0"
    if number.lower() in "demisol":
        return "-1"
    if number == "N/A":
        return "NULL"
    return number


def get_product_type(line):
    my_type = line[5].upper()
    for existing_type in ProductType:
        if my_type == str(existing_type).split(".")[-1]:
            return existing_type
    return ProductType.NULL


def get_furnish_type(line):
    my_type = line[6].upper()
    for existing_type in FurnishType:
        if my_type == str(existing_type).split(".")[-1]:
            return existing_type
    return FurnishType.NULL


def get_number_of_floors(line):
    number_of_floors = line[9]
    if number_of_floors == "N/A":
        return "NULL"
    return number_of_floors


class DataPreparation:

    def __init__(self):
        print("Data preparation...")

        with open(url_csv_scrapped, "r") as fs:
            print(fs.readline().replace("\n", "").split(","))
            line = fs.readline().replace("\n", "")

            features = ["size", "location", "year", "rooms", "type", "furnish", "floor", "total_floors", "price"]
            global products, locations, history_list
            while line:
                line = line.split(",")
                if len(line) >= 13:
                    new_date = [line[0] + line[1]]
                    line = new_date + line[2:]

                product, history, location = self.process_line_for_db(line)
                # features = self.process_for_machine_learning(product, history, location
                if product and product not in products:
                    products.append(product)
                elif product is not None:
                    product_ = [p for p in products if p == product]
                    history.product_id = product_[0].id

                if history and history not in history_list:
                    history_list.append(history)
                if location and location.address not in locations:
                    locations[location.address] = location.id
                line = fs.readline().replace("\n", "")

            self.make_csv()

            # analyse_data.check_relevant_features(features_columns, products)

    def process_for_machine_learning(self, product, history, location):
        # eliminate data that don't provide information
        if 'N/A' in history.price or nan == history.price:
            return None
        features = [float_or_na(product.size),
                    product.location_id,
                    float_or_na(product.year_of_construction),
                    float_or_na(product.number_of_rooms),
                    product.product_type,
                    product.furnish_type,
                    float_or_na(product.floor_number),
                    float_or_na(product.number_of_floors),
                    float_or_na(history.price)]
        return features

    # filter info and return location, history and product if all is correct; else return Nones
    @staticmethod
    def process_line_for_db(line):
        address = unidecode.unidecode(line[4])
        if address == 'N/A' or len(address) <= 0:
            return None, None, None

        if address in locations.keys():
            location_id = locations[address]
        else:
            location_id = uuid.uuid4()
        location = Location(id=location_id, address=address, city_id=city.id)

        product_size = get_size(line)
        if product_size == "NULL" or float(product_size) < 10 or product_size is nan:
            return None, None, None

        product_id = uuid.uuid4()
        product = Product(id=product_id,
                          product_type=get_product_type(line),
                          furnish_type=get_furnish_type(line),
                          floor_number=get_floor_number(line),
                          number_of_floors=get_number_of_floors(line),
                          size=product_size,
                          year_of_construction=get_year(line),
                          location_id=location_id,
                          number_of_rooms=line[7])
        product_price = line[2]
        if product_price == "N/A":
            return None, None, None
        product_price = float(product_price) * 1000

        history_date = get_date(line)
        if history_date is None:
            return None, None, None

        history_id = uuid.uuid4()
        history = ProductHistory(id=history_id,
                                 product_id=product_id,
                                 date=history_date,
                                 price=product_price,
                                 currency_type="EUR")

        return product, history, location

    @staticmethod
    def make_csv():
        with open("../Data/locations.csv", "w") as fd:
            fd.write("address,locationId,cityId\n")
            for address, location_id in locations.items():
                fd.write(address + "," + str(location_id) + "," + str(city.id) + '\n')
        with open("../Data/products.csv", "w") as fd:
            fd.write("productId,size,locationId,productType,furnishType,floorNumber,numberOfFloors,yearOfConstruction,"
                     "numberOfRooms\n")
            for product in products:
                fd.write(str(product) + '\n')
        with open("../Data/history.csv", "w") as fd:
            fd.write("historyId,productId,date,price,curencyType\n")
            for element in history_list:
                fd.write(str(element) + '\n')
