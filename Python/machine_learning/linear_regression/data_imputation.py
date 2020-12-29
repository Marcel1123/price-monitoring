from entities.furnish_type import FurnishType
from entities.product_type import ProductType
from database import database

# root_path = "..\\..\\..\\Data\\"
root_path = "..\\Data\\"


def get_default_values():
    default_values = dict()
    default_values['product_type'] = get_default_type(ProductType)
    default_values['furnish_type'] = get_default_type(FurnishType)
    default_values['floor_number'] = get_default_mean('floor_number')
    default_values['number_of_floors'] = get_default_mean('number_of_floors')
    default_values['year_of_construction'] = get_default_mean('year_of_construction')
    default_values['number_of_rooms'] = get_default_mean('number_of_rooms')

    return default_values


def get_default_type(class_type):
    if class_type == ProductType:
        column = 3
    elif class_type == FurnishType:
        column = 4
    else:
        raise ValueError

    d = {i.name: 0 for i in class_type}
    product_list = database.get_all_products()
    for product in product_list:
        if class_type == ProductType and product.product_type != 'NULL':
            d[product.product_type] += 1
        elif class_type == FurnishType and product.furnish_type != 'NULL':
            d[product.furnish_type] += 1

    maximum = -1
    maximum_name = ''
    for i in class_type:
        if d[i.name] > maximum:
            maximum = d[i.name]
            maximum_name = i.name
    d = maximum_name

    return d


def get_default_mean(column_name):
    if column_name == 'floor_number':
        column = 5
    elif column_name == 'number_of_floors':
        column = 6
    elif column_name == 'year_of_construction':
        column = 7
    elif column_name == 'number_of_rooms':
        column = 8
    else:
        raise ValueError

    values_sum = 0
    count = 0

    product_list = database.get_all_products()
    for product in product_list:
        if column_name == 'floor_number' and product.floor_number is not None:
            values_sum += int(product.floor_number)
            count += 1
        elif column_name == 'number_of_floors' and product.number_of_floors is not None:
            values_sum += int(product.number_of_floors)
            count += 1
        elif column_name == 'year_of_construction' and product.year_of_construction is not None:
            values_sum += int(product.year_of_construction)
            count += 1
        elif column_name == 'number_of_rooms' and product.number_of_rooms is not None:
            values_sum += int(product.number_of_rooms)
            count += 1

    return round(values_sum / count, 0)
