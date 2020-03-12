#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 15:11
# @Author  : 叶永彬
# @File    : test_parkVisitorUsed.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import CarType
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/parkVisitorUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
class TestParkVisitorUsed(BaseCase):
    """访客车辆新增、修改、使用流程"""
    def test_addSpecialType(self):
        """新建特殊类型-访客"""
        pass