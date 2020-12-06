class Location:
    def __init__(self, id, city_id, address):
        self.id = id
        self.city_id = city_id
        self.address = address

    def __str__(self):
        return self.id + "," + self.city_id + "," + self.address
