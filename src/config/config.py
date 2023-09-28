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
config module
=========================

Configuration related stuff here.
1个视频通道对应rtsp的url
1个视频通道包含多个预置点viewpoint
1个预置点包含多个热点区aoi
"""

# Author: Awen <26896225@qq.com>
# License: Apache Licence 2.0

import json


class ConfigSet:
    cfg_ = None             # 下发配置
    path2cfg_ = None        # 下发配置路径

    @classmethod
    def load_json(cls, fp):
        try:
            load_dict = None
            cls.path2cfg_ = fp
            with open(fp, 'r', encoding='UTF-8') as load_f:
                load_dict = json.load(load_f)
                load_f.close()
        finally:
            return load_dict

    @classmethod
    def save_json(cls):
        formatted_cfg = json.dumps(cls.cfg_, ensure_ascii=False, indent=2)
        if cls.path2cfg_:
            with open(cls.path2cfg_, 'w', encoding='utf-8') as fp:
                fp.write(formatted_cfg)
                fp.close()

    @classmethod
    def get_cfg(cls, pathtocfg='model_service.cfg'):
        if cls.cfg_ is None:
            cls.cfg_ = cls.load_json(pathtocfg)
        return cls.cfg_

a=1
cfg = ConfigSet.get_cfg()
URL_SOH = cfg['url_soh']
print(URL_SOH)