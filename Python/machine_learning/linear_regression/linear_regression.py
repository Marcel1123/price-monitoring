import pickle
from pprint import pprint
import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from database import database
from entities.furnish_type import FurnishType
from entities.product import Product
from entities.product_type import ProductType
from machine_learning.linear_regression import data_imputation

# for api
root_path = "..\\Data\\"
model_all_features = "machine_learning\\linear_regression\\model_all.sav"
model_size_and_location = "machine_learning\\linear_regression\\model_size_location.sav"

# for model
# root_path = "..\\..\\..\\Data\\"
# model_all_features = "model_all.sav"
# model_size_and_location = "model_size_location.sav"


def convert_locations_from_csv_to_json():
    locations = dict()
    count = 0
    with open(root_path + "locations.csv") as fd:
        fd.readline()
        line = fd.readline()
        while line:
            line = line.split(",")
            locations[line[1]] = count
            count += 1
            line = fd.readline()
    with open(root_path + "locations.json", "w") as fd:
        json.dump(locations, fd)


def load_locations_from_json():
    with open(root_path + 'locations.json') as json_file:
        locations = json.load(json_file)
    return locations


def load_products_from_csv(default, size=False, location=False, product_type=False, furnish_type=False,
                           floor_number=False, number_of_floors=False, year_of_construction=False,
                           number_of_rooms=False):
    products = dict()
    with open(root_path + "products.csv") as fd:
        fd.readline()
        line = fd.readline()
        while line:
            line = line.split(",")

            product = preprocess_csv(default, size=line[1] if size else None,
                                     location_uid=line[2] if location else None,
                                     product_type=line[3] if product_type else None,
                                     furnish_type=line[4] if furnish_type else None,
                                     floor_number=line[5] if floor_number else None,
                                     number_of_floors=line[6] if number_of_floors else None,
                                     year_of_construction=line[7] if year_of_construction else None,
                                     number_of_rooms=line[8] if number_of_rooms else None)

            if not isinstance(product, str):
                products[line[0]] = product

            line = fd.readline()

    lr_input = []
    lr_output = []
    with open(root_path + "history.csv") as fd:
        fd.readline()
        line = fd.readline()
        while line:
            line = line.split(",")
            try:
                lr_input.append(products[line[1]])
                lr_output.append(float(line[3]))
            except:
                pass
            line = fd.readline()

    return lr_input, lr_output


def load_products_from_db(default, size=False, location=False, product_type=False, furnish_type=False,
                          floor_number=False, number_of_floors=False, year_of_construction=False,
                          number_of_rooms=False):
    product_list = database.get_all_products()
    products = dict()
    for product in product_list:
        product_ = preprocess_db(default, size=product.size if size else None,
                                 location_uid=product.location_id if location else None,
                                 product_type=product.product_type if product_type else None,
                                 furnish_type=product.furnish_type if furnish_type else None,
                                 floor_number=product.floor_number if floor_number else None,
                                 number_of_floors=product.number_of_floors if number_of_floors else None,
                                 year_of_construction=product.year_of_construction if year_of_construction else None,
                                 number_of_rooms=product.number_of_rooms if number_of_rooms else None)

        if not isinstance(product_, str):
            products[product.id] = product_

    lr_input = []
    lr_output = []
    history_list = database.get_all_history()
    for history in history_list:
        try:
            lr_input.append(products[history.product_id])
            lr_output.append(history.price)
        except:
            pass

    return lr_input, lr_output


def preprocess_csv(default, size, location_uid, product_type=None, furnish_type=None, floor_number=None,
                   number_of_floors=None, year_of_construction=None, number_of_rooms=None):
    locations = load_locations_from_json()
    product_type_dict = {i.name: i.value for i in ProductType}
    furnish_type_dict = {i.name: i.value for i in FurnishType}
    # TODO: To use only the last date for every product

    product = []
    if number_of_rooms is not None and number_of_rooms != 'NULL\n':
        number_of_rooms = int(number_of_rooms[:-1])
        if number_of_rooms <= 0 or number_of_rooms > 50:
            return "Invalid number of rooms."
        product.append(number_of_rooms)
    else:
        product.append(default['number_of_rooms'])

    if size is not None and size != 'NULL':
        size = float(size)
        if size <= 0:
            return "Size must be a positive value."
        if number_of_rooms is not None and number_of_rooms != 'NULL\n' \
                and (number_of_rooms * 100 < size or number_of_rooms * 10 > size):
            return "Given size is invalid for the given number of rooms."
        product.append(size)
    else:
        return "Size cannot be null."

    if location_uid:
        try:
            product.append(locations[location_uid])
        except:
            return "Invalid location."
    else:
        return "Location cannot be null."

    if product_type:
        if product_type_dict[product_type] != "NULL":
            product.append(int(product_type_dict[product_type]))
        else:
            product.append(default['product_type'])

    if furnish_type:
        if furnish_type_dict[furnish_type] != "NULL":
            product.append(int(furnish_type_dict[furnish_type]))
        else:
            product.append(default['furnish_type'])

    if number_of_floors is not None and number_of_floors != 'NULL':
        number_of_floors = int(number_of_floors)
        if number_of_floors < 0 or number_of_floors > 150:
            return "Invalid number of floors."
        product.append(number_of_floors)
    else:
        product.append(default['number_of_floors'])

    if floor_number is not None and floor_number != 'NULL':
        floor_number = int(floor_number)
        if number_of_floors is not None and floor_number > number_of_floors:
            return "Floor number can't be greater than total number of floors."
        if floor_number < 0 or floor_number > 150:
            return "Invalid floor number."
        product.append(floor_number)
    else:
        product.append(default['floor_number'])

    if year_of_construction is not None and year_of_construction != 'NULL':
        year_of_construction = int(year_of_construction)
        if year_of_construction < 1900 or year_of_construction > 2050:
            return "Invalid year of construction."
        product.append(year_of_construction)
    else:
        product.append(default['year_of_construction'])

    return product


def preprocess_db(default, size, location_uid, product_type=None, furnish_type=None, floor_number=None,
                  number_of_floors=None, year_of_construction=None, number_of_rooms=None):
    locations = load_locations_from_json()
    product_type_dict = {i.name: i.value for i in ProductType}
    furnish_type_dict = {i.name: i.value for i in FurnishType}
    # TODO: To use only the last date for every product

    product = []
    if number_of_rooms is not None:
        number_of_rooms = int(number_of_rooms)
        if number_of_rooms <= 0 or number_of_rooms > 50:
            return "Invalid number of rooms."
        product.append(number_of_rooms)
    else:
        product.append(default['number_of_rooms'])

    if size is not None:
        size = float(size)
        if size <= 0:
            return "Size must be a positive value."
        if number_of_rooms is not None and number_of_rooms != 'NULL\n' \
                and (number_of_rooms * 100 < size or number_of_rooms * 10 > size):
            return "Given size is invalid for the given number of rooms."
        product.append(size)
    else:
        return "Size cannot be null."

    if location_uid:
        try:
            product.append(locations[location_uid])
        except:
            return "Invalid location."
    else:
        return "Location cannot be null."

    if product_type:
        if product_type_dict[product_type] != "NULL":
            product.append(int(product_type_dict[product_type]))
        else:
            product.append(default['product_type'])

    if furnish_type:
        if furnish_type_dict[furnish_type] != "NULL":
            product.append(int(furnish_type_dict[furnish_type]))
        else:
            product.append(default['furnish_type'])

    if number_of_floors is not None:
        number_of_floors = int(number_of_floors)
        if number_of_floors < 0 or number_of_floors > 150:
            return "Invalid number of floors."
        product.append(number_of_floors)
    else:
        product.append(default['number_of_floors'])

    if floor_number is not None:
        floor_number = int(floor_number)
        if number_of_floors is not None and floor_number > number_of_floors:
            return "Floor number can't be greater than total number of floors."
        if floor_number < 0 or floor_number > 150:
            return "Invalid floor number."
        product.append(floor_number)
    else:
        product.append(default['floor_number'])

    if year_of_construction is not None:
        year_of_construction = int(year_of_construction)
        if year_of_construction < 1900 or year_of_construction > 2050:
            return "Invalid year of construction."
        product.append(year_of_construction)
    else:
        product.append(default['year_of_construction'])

    return product


def create_model(model_path, size=True, location=True, product_type=True, furnish_type=True, floor_number=True,
                 number_of_floors=True, year_of_construction=True, number_of_rooms=True):
    default = data_imputation.get_default_values()
    lr_input, lr_output = load_products_from_db(default, size=size, location=location,
                                                product_type=product_type,
                                                furnish_type=furnish_type,
                                                floor_number=floor_number,
                                                number_of_floors=number_of_floors,
                                                year_of_construction=year_of_construction,
                                                number_of_rooms=number_of_rooms)
    lr_input, lr_output = np.array(lr_input, dtype=object), np.array(lr_output)
    lr_input = PolynomialFeatures(degree=2, include_bias=False).fit_transform(lr_input)
    model = LinearRegression().fit(lr_input, lr_output)
    pickle.dump(model, open(model_path, 'wb'))


def load_model(model_path):
    return pickle.load(open(model_path, 'rb'))


def estimate_price(product):
    model = load_model(model_all_features)
    default = data_imputation.get_default_values()
    input_x = [preprocess_db(default, product.size, product.location_id, product.product_type, product.furnish_type,
                             product.floor_number, product.number_of_floors, product.year_of_construction,
                             product.number_of_rooms)]
    if isinstance(input_x[0], str):
        return input_x[0]
    input_x = PolynomialFeatures(degree=2, include_bias=False).fit_transform(input_x)
    output_y = model.predict(input_x)
    if output_y > 0:
        return int(float(output_y))
    else:
        return "Unable to calculate price due to lack of data for similar products."


def estimate_price_considering_size_and_location(product):
    model = load_model(model_size_and_location)
    default = data_imputation.get_default_values()
    input_x = [preprocess_db(default, product.size, product.location_id)]
    input_x = PolynomialFeatures(degree=2, include_bias=False).fit_transform(input_x)
    output_y = model.predict(input_x)
    return int(float(output_y))


if __name__ == '__main__':
    convert_locations_from_csv_to_json()
    create_model(model_path=model_all_features)
    create_model(model_path=model_size_and_location, product_type=False, furnish_type=False, floor_number=False,
                 number_of_floors=False, year_of_construction=False, number_of_rooms=False)

    my_product_1 = Product("bdc1d015-0a37-48bb-abc9-c3fa5aaa164b", "HOUSE", "FURNISHED", "NULL",
                           "NULL", "136", "2019", "665e1fb1-2622-4ac4-9750-c9dbff5fad72", "5\n")   # 110.000
    my_product_2 = Product("a260f9b8-542b-4603-8aed-e8ff8b20c73f", "SEMI_DETACHED", "UNFURNISHED",
                           "9", "9", "43", "2020", "665e1fb1-2622-4ac4-9750-c9dbff5fad72", "2\n")  # 43.000
    my_product_3 = Product("e1433dbd-e4be-43bd-8fcb-da3f6aee997f", "HOUSE", "FURNISHED", "NULL",
                           "NULL", "400", "2020", "68169837-39df-467b-bccd-5ebbd8d6aeed", "0\n")   # 500.000
    my_product_4 = Product("6c8e8511-6ac6-48f0-b990-6ea75a20c851", "DETACHED", "UNFURNISHED",
                           "0", "4", "44", "2020", "2997d39e-090f-46f2-99fe-e4c5c5ef21d8", "2\n")    # 58.200
    my_product_5 = Product(id="6c8e8511-6ac6-48f0-b990-6ea75a20c852",
                           product_type="SEMI_DETACHED",
                           furnish_type="FURNISHED",
                           floor_number=2,
                           number_of_floors=3,
                           size=43,
                           year_of_construction=2019,
                           location_id="6c2f4e70-a6e4-4d30-87a6-4cfd046ce0ff",
                           number_of_rooms="2\n")  # 40.000
    # these do not work with db preprocess, should work after refactor
    # print(estimate_price(my_product_1))
    # print(estimate_price(my_product_2))
    # print(estimate_price(my_product_3))
    # print(estimate_price(my_product_4))
    # print(estimate_price(my_product_5))
    # print(estimate_price_considering_size_and_location(my_product_5))
