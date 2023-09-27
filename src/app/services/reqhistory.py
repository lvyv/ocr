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
business logic layer
=========================

business logic层，负责实现客户端请求的结果入库和查询。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from app.services.main import AppService
from app.models.dao_reqhistory import RequestHistoryCRUD
from app.utils.service_result import ServiceResult
# from utils.app_exceptions import AppException


class ReqHistoryService(AppService):
    def update_item(self, reqid, res) -> ServiceResult:
        req_item = RequestHistoryCRUD(self.db).update_record(reqid, res)
        if not req_item:
            # return ServiceResult(AppException.FooCreateItem())
            pass
        return ServiceResult(req_item)

    def get_item(self, item_id: int) -> ServiceResult:
        req_item = RequestHistoryCRUD(self.db).get_record(item_id)
        # if not req_item:
        #     return ServiceResult(AppException.FooGetItem({"item_id": item_id}))
        # if not req_item.public:
        #     return ServiceResult(AppException.FooItemRequiresAuth())
        return ServiceResult(req_item)
