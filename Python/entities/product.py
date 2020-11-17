class Product:
    def __init__(self, id, product_type, furnish_type, floor_number, number_of_floors, size,
                 year_of_construction, location_id, number_of_rooms):
        self.id = id
        self.product_type = product_type
        self.furnish_type = furnish_type
        self.floor_number = floor_number
        self.number_of_floors = number_of_floors
        self.size = size
        self.year_of_construction = year_of_construction
        self.location_id = location_id
        self.number_of_rooms = number_of_rooms

    def __str__(self):
        return self.size + " " + self.location_id + " " + self.number_of_rooms + " " + self.product_type + " " + self.furnish_type + " " + self.year_of_construction