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
constants module
=========================

定义所有常量。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from config.config import ConfigSet

cfg = ConfigSet.get_cfg()
# 所有后端的科学计算模型，MODEL类型
MDL_IMGAGE_OUTLINE = 'image_outline'
# DEV_VRLA = 'vrla'
# DEV_CELLPACK = 'cellpack'
# DEV_CANNED_MOTOR_PUMP = 'canned motor pump'
# DEV_CENTRIFUGAL_PUMP = 'centrifugal pump'
# DEV_AC_FAN = 'air conditioner fan'
# DEV_CHILLER = 'chiller'

# 各种状态常量
REQ_STATUS_PENDING = 'pending'
REQ_STATUS_SETTLED = 'settled'

# 后台ai模型的地址
REST_REQUEST_TIMEOUT = 10

# 后台ai模型的地址
URL_SOH = cfg['url_soh']
URL_CLUSTER = cfg['url_cluster']
# 后台ai模型mock的地址
# AIURL_SOH = 'https://127.0.0.1:29083/api/v1/soh'


# phmMS启动的地址、端口、证书等
SCHEDULE_HOST = cfg['schedule_host']
SCHEDULE_PORT = cfg['schedule_port']
SCHEDULE_KEY = cfg['schedule_key']
SCHEDULE_CER = cfg['schedule_cer']
PROMPT_SUFFIX = cfg['prompt_suffix']
OPEN_AI_HTTP_PROXY = cfg['http_proxy']
OPEN_AI_KEY = cfg['open_ai_key']
OPEN_AI_ORG = cfg['open_ai_org']
OPEN_AI_MODEL = cfg['chatgpt_model']
SAM_MODEL_PATH = cfg['sam_model']


