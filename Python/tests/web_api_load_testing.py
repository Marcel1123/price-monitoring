"""
To run this, right click the "tests" package and select "Open in terminal".
    Then, write "locust -f web_api_load_testing.py" and go to http://localhost:8089/
"""
import json
import random

from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(5, 10)
    product_types = ['DETACHED', 'SEMI_DETACHED', 'NON_DETACHED', 'STUDIO', 'HOUSE', 'NULL']
    furnish_types = ['FURNISHED', 'SEMI_FURNISHED', 'UNFURNISHED', 'NULL']

    @task
    def predict_price(self):
        headers = {'content-type': 'application/json'}
        number_of_floors = random.randint(-1, 25)
        floor_number = random.randint(-1, number_of_floors)
        json_data = {
            "product_type": random.choice(self.product_types),
            "furnish_type": random.choice(self.furnish_types),
            "floor_number": floor_number,
            "number_of_floors": number_of_floors,
            "size": random.uniform(30.0, 300.0),
            "year_of_construction": random.randint(1980, 2025),
            "location_id": "6c2f4e70-a6e4-4d30-87a6-4cfd046ce0ff",
            "number_of_rooms": random.randint(1, 10)
        }
        self.client.post("http://localhost:8000/predict-new-product", data=json.dumps(json_data), headers=headers)
