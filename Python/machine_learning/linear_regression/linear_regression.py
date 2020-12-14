import numpy as np
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from entities.furnish_type import FurnishType
from entities.product import Product
from entities.product_type import ProductType

root_path = "..\\..\\..\\Data\\"


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


def load_products_from_csv(size=False, location=False, product_type=False, furnish_type=False, floor_number=False,
                           number_of_floors=False, year_of_construction=False, number_of_rooms=False):
    products = dict()
    with open(root_path + "products.csv") as fd:
        fd.readline()
        line = fd.readline()
        while line:
            line = line.split(",")

            product = preprocess(size=line[1] if size else None,
                                 location_uid=line[2] if location else None,
                                 product_type=line[3] if product_type else None,
                                 furnish_type=line[4] if furnish_type else None,
                                 floor_number=line[5] if floor_number else None,
                                 number_of_floors=line[6] if number_of_floors else None,
                                 year_of_construction=line[7] if year_of_construction else None,
                                 number_of_rooms=line[8] if number_of_rooms else None)

            products[line[0]] = product

            line = fd.readline()

    lr_input = []
    lr_output = []
    with open(root_path + "history.csv") as fd:
        fd.readline()
        line = fd.readline()
        while line:
            line = line.split(",")
            lr_input.append(products[line[1]])
            lr_output.append(float(line[3]))
            line = fd.readline()

    return lr_input, lr_output


def create_model_size_and_location():
    lr_input, lr_output = load_products_from_csv(size=True, location=True)
    lr_input, lr_output = np.array(lr_input), np.array(lr_output)
    lr_input = PolynomialFeatures(degree=2, include_bias=False).fit_transform(lr_input)
    model = LinearRegression().fit(lr_input, lr_output)
    return model


def estimate_price_size_and_location(product_size, location_uid):
    model = create_model_size_and_location()
    locations = load_locations_from_json()
    input_x = [[product_size, locations[location_uid]]]
    input_x = PolynomialFeatures(degree=2, include_bias=False).fit_transform(input_x)
    output_y = model.predict(input_x)
    print(int(float(output_y)))


def create_model_all_features():
    lr_input, lr_output = load_products_from_csv(size=True, location=True, product_type=True, furnish_type=True,
                                                 floor_number=True, number_of_floors=True, year_of_construction=True,
                                                 number_of_rooms=True)
    lr_input, lr_output = np.array(lr_input), np.array(lr_output)
    lr_input = PolynomialFeatures(degree=2, include_bias=False).fit_transform(lr_input)
    model = LinearRegression().fit(lr_input, lr_output)
    return model


def preprocess(size, location_uid, product_type, furnish_type, floor_number, number_of_floors, year_of_construction,
               number_of_rooms):
    locations = load_locations_from_json()
    product_type_dict = {i.name: i.value for i in ProductType}
    furnish_type_dict = {i.name: i.value for i in FurnishType}
    # TODO: To find another method for data imputation
    # TODO: To use only the last date for every product
    default_product_type = 1
    default_furnish_type = 1
    default_floor_number = 1
    default_year_of_construction = 2010
    default_number_of_rooms = int(float(size) / 30)
    default_number_of_floors = 4

    product = []
    if size:
        product.append(float(size))

    if location_uid:
        product.append(locations[location_uid])

    if product_type:
        if product_type_dict[product_type] != "NULL":
            product.append(int(product_type_dict[product_type]))
        else:
            product.append(default_product_type)

    if furnish_type:
        if furnish_type_dict[furnish_type] != "NULL":
            product.append(int(furnish_type_dict[furnish_type]))
        else:
            product.append(default_furnish_type)

    if floor_number:
        if floor_number != "NULL":
            product.append(int(floor_number))
        else:
            product.append(default_floor_number)

    if number_of_floors:
        if number_of_floors != "NULL":
            product.append(int(number_of_floors))
        else:
            product.append(default_number_of_floors)

    if year_of_construction:
        if year_of_construction != "NULL":
            product.append(int(year_of_construction))
        else:
            product.append(default_year_of_construction)

    if number_of_rooms:
        if number_of_rooms != "NULL" and number_of_rooms != "NULL\n":
            product.append(int(number_of_rooms))
        else:
            product.append(default_number_of_rooms)

    return product


def estimate_price_with_features(product):
    model = create_model_all_features()
    input_x = [preprocess(product.size, product.location_id, product.product_type, product.furnish_type,
                          product.floor_number, product.number_of_floors, product.year_of_construction,
                          product.number_of_rooms)]
    input_x = PolynomialFeatures(degree=2, include_bias=False).fit_transform(input_x)
    output_y = model.predict(input_x)
    return int(float(output_y))


if __name__ == '__main__':
    convert_locations_from_csv_to_json()
    estimate_price_size_and_location(100, 'b560dd48-4015-4d53-a2b3-756b0af892af')

    my_product_1 = Product("bdc1d015-0a37-48bb-abc9-c3fa5aaa164b", "HOUSE", "FURNISHED", "NULL",
                           "NULL", "136", "2019", "665e1fb1-2622-4ac4-9750-c9dbff5fad72", "5")  # 110000
    my_product_2 = Product("a260f9b8-542b-4603-8aed-e8ff8b20c73f", "SEMI_DETACHED", "UNFURNISHED",
                           "9", "9", "43", "2020", "665e1fb1-2622-4ac4-9750-c9dbff5fad72", "2")  # 43.000
    my_product_3 = Product("e1433dbd-e4be-43bd-8fcb-da3f6aee997f", "HOUSE", "FURNISHED", "NULL",
                           "NULL", "400", "2020", "68169837-39df-467b-bccd-5ebbd8d6aeed", "0")  # 500.000
    my_product_4 = Product("6c8e8511-6ac6-48f0-b990-6ea75a20c851", "DETACHED", "UNFURNISHED",
                           "0", "4", "44", "2020", "2997d39e-090f-46f2-99fe-e4c5c5ef21d8", 2)  # 58200
    print(estimate_price_with_features(my_product_1))
    print(estimate_price_with_features(my_product_2))
    print(estimate_price_with_features(my_product_3))
    print(estimate_price_with_features(my_product_4))
