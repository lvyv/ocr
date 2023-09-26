import uvicorn
import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import Union, List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    result = None
    for file in files:
        file_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
        result = ocr.ocr(image, cls=True)
        # print(content.decode('utf-8'))
    return result


if __name__ == '__main__':
    uvicorn.run(app, port=8014)
