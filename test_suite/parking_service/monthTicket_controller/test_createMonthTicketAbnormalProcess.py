#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 14:35
# @Author  : 何涌
# @File    : test_createMonthTicketAbnormalProcess.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.parking_service.monthTicket_service import monthTicket_controller
from Api.information_service.information_controller import Information_controller
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service
import time

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parking_service/monthTicket_controller/createMonthTicketAbnormalProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestCreateMonthTicketAbnormalProcess():
    """智泊云车场，临时车进出场，不是月票"""

    # 月票类型创建
    def test_create_vip_type(self,userLogin,send_data,expect):
        re = monthTicket_controller(userLogin).save_monthTicketType(send_data["ticketName"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message"])

    # 开通月票
    def test_open_vip(self,userLogin,send_data,expect):
        re = monthTicket_controller(userLogin).open_monthTicket(send_data["carNum"], send_data["ticketName"])
        result = re.json()
        Assertions().assert_in_text(result,expect["message2"])

    # 开通月票后，非VIP进车
    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum2"])
        Assertions().assert_in_text(result, expect["carType"])

    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information_controller().centralPay(send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    # 开通过期月票后出车
    def test_mockCarOut(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, expect["outscreen"])
        Assertions().assert_in_text(result, expect["outvoice"])

    def test_CarLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, send_data["carNum2"])


