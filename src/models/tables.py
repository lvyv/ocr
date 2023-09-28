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
table data model module
=========================

数据库的表结构的映射模型。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

from sqlalchemy import Column, Integer, String, FLOAT, INTEGER
from config.database import Base, create_tables


class TReqHistory(Base):
    """
    在phmMS收到REST调用时，创建一条记录，保存该异步请求，之后调用phmMD。
    在phmMD被调用启动的工作线程完成耗时计算后，反向回调phmMS，保存原来异步请求的执行结果。
    该表主要字段：
        id: 记录请求号，每次调用都是唯一的；
        model: 记录请求是针对哪个模型；
        status: 该请求的执行状态；
        result: 请求执行的结果。
        requestts: 客户端调用的时间戳。
        settledts: Ai模型执行完成的时间戳。
        memo: 放设备id。
    Attributes
    ----------

    Methods
    -------

    """
    __tablename__ = "req_history"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    status = Column(String)
    result = Column(String)
    requestts = Column(Integer)
    settledts = Column(Integer)
    memo = Column(String, default='')


class TApiToken(Base):
    """
    令牌表，暂存api访问令牌，便于使用。
    该表主要字段：
        id: 记录权限Token；
        url: api的原型，https://ip:port/api/v1/phm/{soh}；
        tk: 该api的访问令牌。

    Attributes
    ----------

    Methods
    -------

    """
    __tablename__ = "api_token"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    tk = Column(String)


class TEquipment(Base):
    """
    令牌表，暂存api访问令牌，便于使用。
    该表主要字段：
        id: 记录权限Token；
        url: api的原型，https://ip:port/api/v1/phm/{soh}；
        tk: 该api的访问令牌。

    Attributes
    ----------

    Methods
    -------

    """
    __tablename__ = "public.xc_equipment"

    ts = Column(Integer, primary_key=True, index=True)
    did = Column(String,  primary_key=True, index=True, default='d01')

    devclass = Column(String, default='BATTERY')

    dis_voltage = Column(FLOAT, default=0)
    dis_current = Column(FLOAT, default=0)
    dis_resistance = Column(FLOAT, default=0)
    dis_temperature = Column(FLOAT, default=0)
    dis_dischargecycles = Column(INTEGER, default=0)

    chg_voltage = Column(FLOAT, default=0)
    chg_current = Column(FLOAT, default=0)
    chg_resistance = Column(FLOAT, default=0)
    chg_temperature = Column(FLOAT, default=0)
    chg_dischargecycles = Column(INTEGER, default=0)
    soh = Column(FLOAT, default=0)
    soc = Column(FLOAT, default=0)
    Rimbalance = Column(FLOAT, default=0)


# create all tables
TABLES = create_tables()
