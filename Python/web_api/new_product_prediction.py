import time
import uuid

import uvicorn

from typing import Optional
from fastapi import FastAPI, Body
from fastapi import Request
from pydantic import BaseModel

from entities.product import Product
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
