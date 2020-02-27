#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/24 15:45
# @Author  : 何涌
# @File    : test_noPresenceVipStrictOutProcess.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/noPresenceVipStrictOutProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云")
class TestNoPresenceVipStrictOutProcess():
    """VIP车无在场严出"""

    def test_mockCarOut(self, send_data, expect):
        """模拟月票车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["screen"])
        Assertions().assert_in_text(result, expect["voice"])

    def test_checkMessageOut(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).check_car_in_out(send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkMessageOutMsg"])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])




