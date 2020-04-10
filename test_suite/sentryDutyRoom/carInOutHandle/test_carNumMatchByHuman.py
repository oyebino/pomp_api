#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 10:46
# @Author  : 叶永彬
# @File    : test_carNumMatchByHuman.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/carNumMatchByHuman.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('临时车离场人工匹配')
class TestCarNumMatchByHuman(BaseCase):
    """临时车离场人工匹配"""
    def test_mockCarInA(self,sentryLogin,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNumA'], 0, send_data['inClientID'])
        result = re
        Assertions().assert_in_text(result['voice'], expect["carInVoiceA"])

    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['matchCarNum'],0,send_data['inClientID'])
        result = re
        Assertions().assert_in_text(result['screen'], expect["carInScreen"])
        Assertions().assert_in_text(result['voice'], expect["carInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["carInOpenGate"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["matchCarNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'],send_data['confidence'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_matchCarNumByhuman(self,sentryLogin,send_data,expect):
        """人工匹配车牌"""
        re = CarInOutHandle(sentryLogin).matchCarNum(send_data['carNum'],send_data['matchCarNum'])
        result = re
        Assertions().assert_in_text(result['leaveCarNo'], expect["matchCarNumMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['matchCarNum'],send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["matchCarNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
