THRESHOLD = 0.001


def compare(product_11, product_2):
    return distance_between_products(product_11, product_2) < THRESHOLD


def distance_between_products(product_1, product_2):
    return 0.01


class IdenticalProducts:
    def __init__(self):
        print("init bd")
