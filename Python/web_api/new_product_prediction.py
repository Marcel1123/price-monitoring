import time
import uuid

import uvicorn

from typing import Optional
from fastapi import FastAPI, Body
from fastapi import Request
from pydantic import BaseModel

from entities.furnish_type import FurnishType
from entities.product import Product
from entities.product_type import ProductType
from machine_learning.linear_regression import linear_regression

app = FastAPI()


class ProductRequest(BaseModel):
    size: float
    location_id: str
    product_type: Optional[str] = Body(None)
    furnish_type: Optional[str] = Body(None)
    floor_number: Optional[int] = Body(None)
    number_of_floors: Optional[int] = Body(None)
    year_of_construction: Optional[int] = Body(None)
    number_of_rooms: Optional[int] = Body(None)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"request processed in {process_time} s")
    return response


@app.post("/predict-new-product")
def predict_new_product_price(product: ProductRequest):
    if product.size <= 0:
        return {"message": "Size must be a positive number"}
    if len(product.location_id) == 0:
        return {"message": "Location id cannot be empty"}
    if product.product_type is not None:
        try:
            ProductType[product.product_type]
        except:
            return {"message": "Invalid product type that isn't null"}
    if product.furnish_type is not None:
        try:
            FurnishType[product.furnish_type]
        except:
            return {"message": "Invalid furnish type that isn't null"}
    if product.number_of_floors is not None and product.number_of_floors < 0:
        return {"message": "Number of floors cannot be negative"}
    if product.year_of_construction is not None and product.year_of_construction < 1900:
        return {"message": "Invalid year of construction that isn't null"}
    if product.number_of_rooms is not None and product.number_of_rooms < 0:
        return {"message": "Number of rooms cannot be negative"}
    product_ = Product(id=uuid.uuid4(),
                       product_type=product.product_type,
                       furnish_type=product.furnish_type,
                       floor_number=product.floor_number,
                       number_of_floors=product.number_of_floors,
                       size=product.size,
                       year_of_construction=product.year_of_construction,
                       location_id=product.location_id,
                       number_of_rooms=product.number_of_rooms)
    return {"message": linear_regression.estimate_price(product_)}


if __name__ == "__main__":
    uvicorn.run("new_product_prediction:app")
