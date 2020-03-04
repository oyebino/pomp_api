#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/07 14:35
# @Author  : 何涌
# @File    : test_monthTicketFullPositionStrictInVipCharge.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/monthTicketFullPositionControl/monthTicketFullPositionStrictInVipCharge.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestMonthTicketFullPositionStrictInVipCharge(BaseCase):
    """VIP类型满位限行（系统有空位自动放行，无空位手动放行按VIP计费）"""

    # 满位VIP第一辆车进车
    def test_mockCarIn1(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar1(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum"])
        Assertions().assert_in_text(result, expect["ticketName"])

    # 满位VIP第二辆车进车
    def test_mockCarIn2(self, send_data, expect):
        re = cloudparking_service().mockCarInOut(send_data['carNum2'],0,send_data['inClientID'])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage2"])
        Assertions().assert_in_text(result, expect["inscreen2"])
        Assertions().assert_in_text(result, expect["invoice2"])

    def test_checkMessageoutn(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum2'])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkMessageInMsg"])

    def test_presentCar2(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage2"])
        Assertions().assert_in_text(result, expect["carNum2"])
        Assertions().assert_in_text(result, expect["carType2"])

    # 满位VIP第一辆车出车
    def test_mockCarOut1(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])

    def test_CarLeaveHistory1(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, expect["carNum"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOut2(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum2"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOut2Msg"])
        Assertions().assert_in_text(result, expect["outscreen2"])
        Assertions().assert_in_text(result, expect["outvoice2"])

    def test_CarLeaveHistory2(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage2"])
        Assertions().assert_in_text(result, expect["carNum2"])