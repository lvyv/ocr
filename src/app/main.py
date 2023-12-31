#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 The CASICloud Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

"""
=========================
entrypoint of the app
=========================

三层架构应用程序的主入口.
"""
import requests
import uvicorn
import cv2
import numpy as np
from app.utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from app.routers import img_outline, reqhistory
from app.routers.common import img_queue
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from ocr import get_ocr
from app.utils.app_exceptions import app_exception_handler
import threading
import app.models.tables as tb
from fastapi.staticfiles import StaticFiles
from multiprocessing import Process
# from Rest import get_image_and_ocr_and_result
# import config.constants as ct
import logging
import urllib.parse
import openai
from hdbscan import get_merged_polygon_for_hdbscan
from extract_the_result import load_action_prompt
from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# 图片识别任务Worker进程
def get_image_and_ocr_and_result(file):
    res = []
    try:
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        rectangles = get_ocr(image)
        logger.info(f'1. OCR ended.')
        characters = get_merged_polygon_for_hdbscan(rectangles)
        logger.info(f'2. Clustering ended.')
        # get prompt from file.
        orc_prompt = load_action_prompt(AiCmdEnum.orc)
        raise(openai.error.AuthenticationError('This is a temparory error.'))   #  临时加入，可以注释掉
        result = chat_with_prompt_for_pic(orc_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=characters)
        logger.info(f'3. LLM ended.')
        logger.info(f'{characters}\n{orc_prompt}\n{result}')
        res = result.split('\n')       # noqa
    except openai.error.AuthenticationError as err:
        logger.error(err)
        res = [rectangles, characters]    # 出错则返回rectangles矩形，聚类结果
    finally:
        return res


def img_deal(queue):
    logger.info(f'OCR process img_deal starting...')
    while True:
        item = queue.get()
        logger.info(f'OCR task confirmed.')
        pid = item.id
        img_list = item.img

        i = 0
        results = {}
        for file in img_list:
            i += 1

            img = "picture{}".format(i)

            result = get_image_and_ocr_and_result(file)
            results[img] = result

        # 用requests上传results
        encoded_params = urllib.parse.urlencode(results)
        base_url = "http://127.0.0.1:29081/api/v1/reqhistory/item/?reqid={}&res={}".format(pid, encoded_params)

        response = requests.put(base_url, data=encoded_params)

        if response.status_code == requests.codes.ok:
            print("PUT请求成功！")
        else:
            print("PUT请求失败！")
        print(results)


# FastAPI进程
app = FastAPI(
    title="图片识别与内容提取微服务",
    description="图片识别与内容提取微服务对外发布的REST API接口",
    version="0.1.0",
)
app.mount('/static', StaticFiles(directory='../swagger_ui_dep/static'), name='static')
logger.info(f'Worker Thread: {threading.current_thread().ident:6}     tables {tb.TABLES}.')


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(img_outline.router)
app.include_router(reqhistory.router)


def run():
    """Test app.main:app"""
    img_deal_process = Process(target=img_deal, args=(img_queue,))
    img_deal_process.start()
    logger.info(f'********************  XBCX AI services  ********************')
    # logging.info(f'Task tables were created by import statement {tb.TABLES}.')
    # logging.info(f'AI micro service starting at {ct.SCHEDULE_HOST}: {ct.SCHEDULE_PORT}')
    uvicorn.run('app.main:app',  # noqa 标准用法
                host='0.0.0.0',
                port=29081,
                # ssl_keyfile=ct.SCHEDULE_KEY,
                # ssl_certfile=ct.SCHEDULE_CER,
                # log_level='info',
                # workers=3
                )


if __name__ == '__main__':
    run()
