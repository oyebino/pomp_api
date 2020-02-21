#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 11:15
# @Author  : 叶永彬
# @File    : test_carInOutCastNum.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/useParking/lightRuleChannel/carInOutCastNum.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarInOutCastNum(BaseCase):
    """临时车进出场识别错-车牌强制转换为正确车牌"""
    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNumIn'],0,send_data['inClientID'])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"],send_data["actualCarNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data['carNumOut'],1,send_data['outClientID'])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).normal_car_out(send_data["parkUUid"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkId"],send_data["actualCarNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["parkingBillDetailMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["actualCarNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
