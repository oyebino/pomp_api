#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/06 14:35
# @Author  : 何涌
# @File    : test_oneParkingSpaceTwoCarWideInProcess.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/oneParkingSpaceTwoCarWideIn.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestOneParkingSpaceTwoCarWideInProcess():
    """多位多车VIP转临时车宽进"""
    """一位两车VIP进出场流程，第一辆VIP车比第二辆车先离场（不开启在场转VIP）"""

    # 多位多车VIP第一辆车进车
    def test_mockCarIn1(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar1(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum"])
        Assertions().assert_in_text(result, expect["ticketName"])

    # 多位多车VIP第二辆车进车
    def test_mockCarIn2(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen2"])
        Assertions().assert_in_text(result, expect["invoice2"])

    def test_presentCar2(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum2"])
        Assertions().assert_in_text(result, expect["carType"])

    # 多位多车VIP第一辆车出车
    def test_mockCarOut1(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_CarLeaveHistory1(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, expect["carNum"])

    # 第二辆车中央缴费
    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information_controller().centralPay(send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information_controller(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum2"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carNum2"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOut2(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["outscreen2"])
        Assertions().assert_in_text(result, expect["outvoice2"])

    def test_CarLeaveHistory2(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, expect["carNum2"])