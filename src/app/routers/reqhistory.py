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

controller层，负责模型回调路由分发.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import APIRouter, Depends
from app.services.reqhistory import ReqHistoryService
from app.utils.service_result import handle_result
from config.database import get_db
import logging

router = APIRouter(
    prefix="/api/v1/reqhistory",
    tags=["基础微服务"],
    responses={404: {"description": "Not found"}},
)


@router.put("/item/")
async def update_item(reqid: str, res: str, db: get_db = Depends()):
    reqs = ReqHistoryService(db)
    result = reqs.update_item(reqid, res)
    logging.info(f'the submitted task:{reqid} got result - {res} ')
    return handle_result(result)


@router.get("/item/{item_id}")
async def get_item(item_id: int, db: get_db = Depends()):
    result = ReqHistoryService(db).get_item(item_id)
    return handle_result(result)
