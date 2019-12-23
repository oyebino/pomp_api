#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 15:32
# @Author  : 叶永彬
# @File    : test_carInOutDetail.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/information_service/carInOutDetail.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询模块")
class TestCarInOutDetail():
    """车辆进场流程"""
    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information_controller().centralPay(send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information_controller(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["parkingBillDetailMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
