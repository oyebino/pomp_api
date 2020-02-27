#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/12 14:35
# @Author  : 何涌
# @File    : test_carAbnormalIn.py

import pytest,os
import allure
from common.utils import YmlUtils
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/technicalSupport/carAbnormalIn.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestCarAbnormalIn():
    """临时车异常进场"""

    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum"])

    def test_mockCarIn2(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar2(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum"])

    def test_getAbnormalInCar(self, userLogin, send_data, expect):
        """查看异常进场记录"""
        re = Information(userLogin).getAbnormalInCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["AbnormalInCarMessage"])
        Assertions().assert_in_text(result, expect["carNum"])
        Assertions().assert_in_text(result, expect["exceptionType"])

    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information().centralPay(send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carNum"])

    def test_mockCarOut(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["outscreen"])
        Assertions().assert_in_text(result, expect["outvoice"])

    def test_CarLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["carNum"])


