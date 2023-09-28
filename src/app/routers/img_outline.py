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
import cv2
import numpy as np
import time
from fastapi import APIRouter, File, UploadFile, Depends
from app.schemas.reqhistory import ReqItemCreate
from app.services.sv_img_outline import ImageOutlineService
from app.utils.service_result import handle_result, ServiceResult
from app.utils.app_exceptions import AppException
from config.database import get_db
from pydantic import BaseModel
from typing import List
from config import constants as ct
from app.models.dao_reqhistory import RequestHistoryCRUD
from paddleocr import PaddleOCR
import logging

router = APIRouter(
    prefix="/api/v1/image",
    tags=["图片内容提炼模型"],
    responses={404: {"description": "Not found"}},
)


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
        res = None
        # for file in files:
        #     file_bytes = await file.read()
        #     image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        #     ocr = PaddleOCR(use_angle_cls=True,
        #                     lang="ch")  # need to run only once to download and load model into memory
        #     result = ocr.ocr(image, cls=True)
        #     print(content.decode('utf-8'))
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
    return handle_result(res)
