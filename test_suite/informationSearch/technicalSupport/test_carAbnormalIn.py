#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/12 14:35
# @Author  : 何涌
# @File    : test_carAbnormalIn.py

import pytest,os
import allure
from common.utils import YmlUtils
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/technicalSupport/carAbnormalIn.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询-技术支持")
@allure.story('临时车异常进场')
class TestCarAbnormalIn():
    """临时车异常进场"""

    def test_mockCarIn(self, sentryLogin, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["presentCarMessage"])

    def test_mockCarIn2(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar2(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["presentCarMessage"])

    def test_getAbnormalInCar(self, userLogin, send_data, expect):
        """查看异常进场记录"""
        re = Information(userLogin).getAbnormalInCar(send_data["parkName"], send_data["carNum"])
        result = re[0]
        Assertions().assert_text(result['carCode'], expect["abnormalInCar"])
        Assertions().assert_text(result['exceptionType'], expect["exceptionType"])

    def test_mockCarOut(self,sentryLogin, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service(sentryLogin).mockCarInOut(send_data["carNum"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMsg"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['outscreen'])
        Assertions().assert_in_text(result['voice'], expect['outvoice'])
        Assertions().assert_in_text(result['open_gate'], expect['outOpen_gate'])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["parkingBillMsg"])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["carLeaveHistoryMsg"])


