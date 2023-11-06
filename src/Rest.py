# import uvicorn
import cv2
import numpy as np
# from typing import Union, List
# from fastapi import FastAPI, File, UploadFile
# from pydantic import BaseModel
# from hdbscan import get_merged_polygon_for_hdbscan
from extract_the_result import load_action_prompt
# from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum
import logging
from sam import create_tensor
from collections import Counter

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# app = FastAPI()


# @app.post("/upload/")
# async def upload_file(files: List[UploadFile] = File(...)):
#     result = None
#     for file in files:
#         file_bytes = await file.read()
#         image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
#         rectangles = get_ocr(image)
#         characters = get_merged_polygon_for_hdbscan(rectangles)
#
#         # get prompt from file.
#         orc_prompt = load_action_prompt(AiCmdEnum.orc)
#
#         result = chat_with_prompt_for_pic(orc_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)
#
#     return result.split('\n')


def cluster_for_sam(rectangles, tensor):
    chara = {}
    for item in rectangles:
        rec = item[0]
        x0, y0 = rec[0]
        x1, y1 = rec[1]

        labels = tensor[int(y0 - 15):int(y1), int(x0 - 15):int(x1)]

        count = Counter(list(labels.flatten()))
        #     print(count)
        label = 0
        max_label_num = 0
        for i in count:
            if count[i] > max_label_num:
                label = i
                max_label_num = count[i]

        if label not in chara:
            chara[label] = []
        chara[label].append(item[1][0])

    return chara


def get_image_chara_and_prompt(file, rectangles):
    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)

    # tensor = create_tensor(image)
    tensor = np.loadtxt(r'..\tensor.csv', delimiter=',')
    logger.info(f'2. tensor ended.')

    characters = cluster_for_sam(rectangles, tensor)
    logger.info(f'3. Clustering ended.')

    # get prompt from file.
    ocr_prompt = load_action_prompt(AiCmdEnum.orc)
    # result = chat_with_prompt_for_pic(orc_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)
    # logger.info(f'3. LLM ended.')
    logger.info(f'{characters}\n{ocr_prompt}\n')
    return characters


# def get_image_and_ocr_and_result(file):
#
#     image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
#     rectangles = get_ocr(image)
#     logger.info(f'1. OCR ended.')
#     characters = get_merged_polygon_for_hdbscan(rectangles)
#     logger.info(f'2. Clustering ended.')
#     # get prompt from file.
#     ocr_prompt = load_action_prompt(AiCmdEnum.orc)
#     result = chat_with_prompt_for_pic(ocr_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)
#     logger.info(f'3. LLM ended.')
#     logger.info(f'{characters}\n{ocr_prompt}\n{result}')
#     return characters, ocr_prompt


# if __name__ == '__main__':
#     uvicorn.run(app, port=8014)
