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
mock module
=========================

接口测试，用于健康模型构件的接口测试仿真。
同时也是phmMD中模型的参考实现（多线程）。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from time import sleep
import uvicorn
import concurrent.futures
import httpx
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
app = FastAPI()

# 支持跨域
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# IFX:REST 数据资源集成分系统提供的数据服务接口
@app.get("/api/v1/devicetype")
async def calculate_soh(deviceid: str):
    """模拟耗时的机器学习任务"""
    return {'deviceid': deviceid, 'type': 'vrla'}


# IF11:REST MODEL 外部接口-phmMD与phmMS之间仿真接口
# 线程池初始化
executor_ = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def computationally_intensive(sohin, reqid):
    logging.info(f'{sohin}, {reqid}')
    sleep(5)
    with httpx.Client(timeout=None, verify=False) as client:
        r = client.put(f'https://127.0.0.1:29081/api/v1/reqhistory/item/?reqid={reqid}&res={"threading end result."}')
        logging.info(r)
    return 0


class SohInputParams(BaseModel):
    devices: str = '[]'     # json string
    tags: str = '[]'        # json string
    startts: int            # timestamp ms
    duration: int           # ms


@app.post("/api/v1/soh")
async def calculate_soh(sohin: SohInputParams, reqid: int):
    """模拟耗时的机器学习任务"""
    executor_.submit(computationally_intensive, sohin, reqid)
    return {'task': reqid, 'status': 'submitted to work thread.'}


if __name__ == '__main__':
    uvicorn.run('mock:app',                # noqa
                host="0.0.0.0",
                port=29083,
                ssl_keyfile="cert.key",
                ssl_certfile="cert.cer"
                )
