from fastapi import FastAPI
import logging
import uvicorn
import config.constants as ct
import json
from typing import List
from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
from ocr import get_ocr
from fastapi.responses import JSONResponse


# 配置logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app_ocr = FastAPI(
    title="文字识别微服务",
    version="0.1.0",
)


@app_ocr.post("/ocr/")  # 接收图片，将ocr传入队列
async def getocr(files: List[UploadFile] = File(...)):
    for file in files:
        file_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

    rectangles = get_ocr(image)
    # ocr_queue.put(rectangles)
    json_data = json.dumps(rectangles)

    return JSONResponse(content=json_data, media_type="application/json")


@app_ocr.post("/test/")
async def test(files: List[UploadFile] = File(...)):
    for file in files:
        file_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    # 启动fastAPI
    logging.info(f'*********************  OCR AI services  ********************')
    uvicorn.run(app_ocr,
                host='0.0.0.0',
                port=29083,
                ssl_keyfile=ct.SCHEDULE_KEY,
                ssl_certfile=ct.SCHEDULE_CER
                )
