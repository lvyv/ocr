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
basic config module
=========================

定义健康管理模型的各种公共配置。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from config.config import ConfigSet

cfg = ConfigSet.get_cfg()
# phmMD启动的地址、端口、证书等
MODEL_HOST = cfg['model_host']
MODEL_PORT = cfg['model_port']
MODEL_KEY = cfg['model_key']
MODEL_CER = cfg['model_cer']

# RESTFul请求超时期限
REST_REQUEST_TIMEOUT = 1
# 各种MOCK地址
# URL_DEVICETYPE = 'https://127.0.0.1:29083/api/v1/devicetype'
# 创建一个统计指标数据记录
URL_POST_EQUIPMENT = cfg['url_post_equipment']
# 更新历史请求记录
URL_RESULT_WRITEBACK = cfg['url_result_writeback']

# 设备类型
DT_VRLA = 'vrla'
DT_CELLPACK = 'cellpack'
DT_CANNED_MOTOR_PUMP = 'canned motor pump'
DT_CENTRIFUGAL_PUMP = 'centrifugal pump'
DT_CENTRIFUGAL_FAN = 'air conditioner fan'
DT_SCREW_CHILLER = 'chiller'
