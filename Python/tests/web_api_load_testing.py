"""
To run this, right click the "tests" package and select "Open in terminal".
    Then, write "locust -f web_api_load_testing.py" and go to http://localhost:8089/
"""
import json

from locust import HttpUser, task, between


class ApiUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def predict_price(self):
        headers = {'content-type': 'application/json'}
        json_data = {
            "product_type": "DETACHED",
            "furnish_type": "FURNISHED",
            "floor_number": 3,
            "number_of_floors": 8,
            "size": 60.0,
            "year_of_construction": 2019,
            "location_id": "6c2f4e70-a6e4-4d30-87a6-4cfd046ce0ff",
            "number_of_rooms": 3
        }
        self.client.post("http://localhost:8000/predict-new-product", data=json.dumps(json_data),
                         headers=headers, catch_response=True)

# TODO: random values for json; fix ValueError: too many file descriptors in select()
