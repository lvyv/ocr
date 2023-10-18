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
unit test module
=========================

测试模型调度核心模块的入口主进程.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import unittest
import uvicorn
from app import __version__
import app.models.tables as tb
import config.constants as ct
import logging
from app.main import run

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `健康模型构件` entrypoint.
    本测试案例启动整个健康模型构件（可以在数据资源集成分系统的算法开发软件中部署的模型协同工作）
    访问运行本案例的URL：
    https://IP:29081/docs，执行POST /subprocess，发送start/stop命令启停视频识别流水线。
    注意
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_Main(self):
        run()
        """Test app.main:app"""
        # logging.info(f'********************  XBCX AI services  ********************')
        # logging.info(f'Task tables were created by import statement {tb.TABLES}.')
        # logging.info(f'AI micro service starting at {ct.SCHEDULE_HOST}: {ct.SCHEDULE_PORT}')
        # uvicorn.run('app.main:app',  # noqa 标准用法
        #         host=ct.SCHEDULE_HOST,
        #         port=ct.SCHEDULE_PORT,
        #         ssl_keyfile=ct.SCHEDULE_KEY,
        #         ssl_certfile=ct.SCHEDULE_CER,
        #         log_level='warning',
        #         workers=3
        #         )


if __name__ == "__main__":
    unittest.main()
