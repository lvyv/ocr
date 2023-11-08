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
controller layer
=========================

controller层，负责电池模型调用路由分发.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import json
import time
from fastapi import APIRouter, File, UploadFile, Depends
from app.schemas.reqhistory import ReqItemCreate
from app.services.sv_img_outline import ImageOutlineService
from app.utils.service_result import handle_result, ServiceResult
from app.utils.app_exceptions import AppException
from config.database import get_db
from typing import List
from config import constants as ct
from app.models.dao_reqhistory import RequestHistoryCRUD
import logging
from app.routers.common import img_queue
import requests
from Rest import get_image_chara_and_prompt
import os
import urllib.parse
from extract_the_result import load_action_prompt
from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum
from hdbscan import get_merged_polygon_by_hdbscan, get_unmerged_polygon_by_hdbscan

os.environ['NO_PROXY'] = '127.0.0.1'

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/api/v1/image",
    tags=["图片内容提炼模型"],
    responses={404: {"description": "Not found"}},
)


class Content:
    def __init__(self, pid, img_list):
        self.id = pid
        self.img = img_list


# 图片内容提炼模型接口，该层接口可以实现模型与调用方解耦，并添加负载均衡等扩展功能。
@router.post("/outline")
async def outline(files: List[UploadFile] = File(...), db: get_db = Depends()):
    """
    图片内容大纲

    :param files: 上传图片列表。
    :type: SohInputParams。
    :param db: 数据库连接。
    :type: sqlalchemy.orm.sessionmaker。
    :return:
    :rtype:
    """

    try:
        """
        图片内容提炼
        :param devs:
        :param tags:
        :param startts:
        :param endts:
        :return:
        """
        dev_type = ct.MDL_IMGAGE_OUTLINE
        external_data = {
            'model': dev_type,
            'status': ct.REQ_STATUS_PENDING,
            'result': ct.REQ_STATUS_PENDING,
            'requestts': int(time.time() * 1000),
            # 'memo': json.dumps(devs)
        }
        item = ReqItemCreate(**external_data)

        outline_item = RequestHistoryCRUD(db).create_record(item)
        res = ServiceResult(outline_item)
        # 接下来要派发任务到队列，由消费者完成任务，并更新任务
        ImageOutlineService(db, files, res.value.id)

        # res = await bs.soh(json.loads(sohin.devices), json.loads(sohin.tags), sohin.startts, sohin.endts)
    except json.decoder.JSONDecodeError:
        res = ServiceResult(AppException.HttpRequestParamsIllegal())

    for file in files:
        file_bytes = await file.read()
    pro = Content(res.value.id, file_bytes)
    img_queue.put(pro)

    return handle_result(res)


@router.post("/synch")
async def synch(files: List[UploadFile] = File(...)):
    result = None
    for file in files:
        file_bytes = await file.read()

        # 传给OCR
        img_files = [("files", file_bytes)]
        url = f"https://127.0.0.1:29083/ocr/"

        try:
            response = requests.post(url, files=img_files, verify=False)

            if response.status_code == requests.codes.ok:
                print("post ocr请求成功！")
            else:
                print("post ocr请求失败！")

        except requests.exceptions.RequestException as err:
            logger.error(f"OCR fastAPI连接失败！{err}")
            response = None
            result = "OCR fastAPI连接失败！"

        if response is not None:
            # 获取坐标
            data = response.json()
            rectangles = json.loads(data)
            logger.info(f"OCR 获取坐标成功！")

            # 聚类
            chara = get_image_chara_and_prompt(file_bytes, rectangles)
            final = []
            for i in chara.keys():
                final.append(chara[i])
            logger.info(final)

            # 用requests上传chara
            x1 = json.dumps(chara)
            encoded_params = urllib.parse.quote(x1)

            base_url = f"https://127.0.0.1:29082/gpt/?repid=1&chara={encoded_params}"

            try:
                response = requests.put(base_url, data=encoded_params, verify=False)
                result = response.text

            except requests.exceptions.RequestException as err:
                logger.info(f"GPT fastAPI连接失败！{err}")
                result = "GPT fastAPI连接失败！"

    return result


@router.post("/rengong")
async def get_chara(chara: str):
    ocr_prompt = load_action_prompt(AiCmdEnum.ocr)
    result = chat_with_prompt_for_pic(ocr_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=chara)
    return result


@router.post("/hdbscan")
async def use_hdbscan(files: List[UploadFile] = File(...)):
    result = None
    for file in files:
        file_bytes = await file.read()

        # 传给OCR
        img_files = [("files", file_bytes)]
        url = f"https://127.0.0.1:29083/ocr/"

        try:
            response = requests.post(url, files=img_files, verify=False)

            if response.status_code == requests.codes.ok:
                print("post ocr请求成功！")
            else:
                print("post ocr请求失败！")

        except requests.exceptions.RequestException as err:
            logger.error(f"OCR fastAPI连接失败！{err}")
            response = None
            result = "OCR fastAPI连接失败！"

        if response is not None:
            # 获取坐标
            data = response.json()
            rectangles = json.loads(data)
            logger.info(f"OCR 获取坐标成功！")

            # 聚类或不聚类
            post_process = 'HDBSCAN'
            # post_process = 'OCRONLY'
            chara = {}
            if post_process == 'HDBSCAN':
                chara = get_merged_polygon_by_hdbscan(rectangles)
            if post_process == 'OCRONLY':
                chara = get_unmerged_polygon_by_hdbscan(rectangles)
            final = []
            for i in chara.keys():
                final.append(chara[i])
            logger.info(final)

            # 用requests上传chara
            x1 = json.dumps(chara)
            encoded_params = urllib.parse.quote(x1)

            base_url = f"https://127.0.0.1:29082/gpt/?repid=1&chara={encoded_params}&memo={file.filename}&model={post_process}"

            try:
                response = requests.put(base_url, data=encoded_params, verify=False)
                result = response.text
                logger.info(f'*{file.filename}* is successfully processed.')
            except requests.exceptions.RequestException as err:
                logger.info(f"GPT fastAPI连接失败！{err}")
                result = "GPT fastAPI连接失败！"

    return result
