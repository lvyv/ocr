import uvicorn
import cv2
import numpy as np
from typing import Union, List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from ocr import get_ocr
from hdbscan import get_merged_polygon_for_hdbscan
from extract_the_result import load_action_prompt
from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum
import logging

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...)):
    result = None
    for file in files:
        file_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        rectangles = get_ocr(image)
        characters = get_merged_polygon_for_hdbscan(rectangles)

        # get prompt from file.
        orc_prompt = load_action_prompt(AiCmdEnum.orc)

        result = chat_with_prompt_for_pic(orc_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)

    return result.split('\n')


def get_image_and_ocr_and_result(file):

    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    rectangles = get_ocr(image)
    logger.info(f'1. OCR ended.')
    characters = get_merged_polygon_for_hdbscan(rectangles)
    logger.info(f'2. Clustering ended.')
    # get prompt from file.
    orc_prompt = load_action_prompt(AiCmdEnum.orc)
    result = chat_with_prompt_for_pic(orc_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)
    logger.info(f'3. LLM ended.')
    logger.info(f'{characters}\n{orc_prompt}\n{result}')
    return result.split('\n')


if __name__ == '__main__':
    uvicorn.run(app, port=8014)
