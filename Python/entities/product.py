from entities.furnish_type import FurnishType
from entities.product_type import ProductType


class Product:
    def __init__(self, id, floor_number, furnish_type, number_of_floors, number_of_rooms,
                 size, product_type, year_of_construction, location_id):
        self.id = id
        if isinstance(product_type, int):
            self.product_type = ProductType(product_type).name
        else:
            self.product_type = product_type
        if isinstance(furnish_type, int):
            self.furnish_type = FurnishType(furnish_type).name
        else:
            self.furnish_type = furnish_type
        self.floor_number = floor_number
        self.number_of_floors = number_of_floors
        self.size = size
        self.year_of_construction = year_of_construction
        self.location_id = location_id
        self.number_of_rooms = number_of_rooms

    # def __init__(self, id, product_type, furnish_type, floor_number, number_of_floors, size,
    #              year_of_construction, location_id, number_of_rooms):
    #     self.id = id
    #     self.product_type = product_type
    #     self.furnish_type = furnish_type
    #     self.floor_number = floor_number
    #     self.number_of_floors = number_of_floors
    #     self.size = size
    #     self.year_of_construction = year_of_construction
    #     self.location_id = location_id
    #     self.number_of_rooms = number_of_rooms

    def __eq__(self, other):
        return self.size == other.size and \
               self.product_type == other.product_type and \
               self.furnish_type == other.furnish_type and \
               self.floor_number == other.floor_number and \
               self.number_of_floors == other.number_of_floors and \
               self.year_of_construction == other.year_of_construction and \
               self.number_of_rooms == other.number_of_rooms

    def __str__(self):
        return str(self.id) + "," + str(self.size) + "," + str(self.location_id) + "," \
               + self.product_type.name.upper() + ',' + self.furnish_type.name.upper() + "," \
               + self.floor_number + "," + self.number_of_floors + "," + self.year_of_construction + "," \
               + self.number_of_rooms
