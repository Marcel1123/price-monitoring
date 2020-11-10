from entities.product import Product

THRESHOLD = 2


class IdenticalProducts:
    def __init__(self):
        print("init bd")

    def distance_between_products(self, product1, product2):
        score = 0
        if product1.product_type != product2.product_type:
            score += 0.5
        if product1.furnish_type != product2.furnish_type:
            score += 1

        score += abs(product1.floor_number - product2.floor_number)

        score += abs(product1.number_of_floors - product2.number_of_floors) / 10

        score += abs(product1.size - product2.size) / 10

        score += abs(product1.year_of_construction - product2.year_of_construction) / 10

        if product1.location_id != product2.location_id:
            score += 1

        score += abs(product1.number_of_rooms - product2.number_of_rooms)

        return score

    def compare(self, product_11, product_2):
        return self.distance_between_products(product_11, product_2) < THRESHOLD
