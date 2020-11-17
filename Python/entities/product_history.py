class ProductHistory:
    def __init__(self, id, product_id, date, price, currency_type):
        self.id = id
        self.product_id = product_id
        self.date = date
        self.price = price
        self.currency_type = currency_type

    def __str__(self):
        return str(self.date)[:10] + " " + self.price
