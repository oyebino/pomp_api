#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/12 14:35
# @Author  : 何涌
# @File    : test_vipWideInOutProcess.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/vipWideInOutProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestVipWideInOutProcess():
    """纯月票车宽进，不需缴费宽出"""

    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["screen"])
        Assertions().assert_in_text(result, expect["voice"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, send_data["carNum"])
        Assertions().assert_in_text(result, send_data["ticketName"])

    def test_mockCarOut(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["screen"])
        Assertions().assert_in_text(result, expect["voice"])

    def test_CarLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["carNum"])


