#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 9:40
# @Author  : 叶永彬
# @File    : test_centralAdjustCarNum.py


import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/adjustCarNum.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('临时车进出场只校正车牌')
class TestAdjustCarNum(BaseCase):
    """临时车进出场只校正车牌"""
    def test_mockCarIn(self,sentryLogin,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNum'], 0, send_data['inClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMsg"])

    def test_adjustCarInNum(self,sentryLogin,send_data,expect):
        """校正进场车辆"""
        re = CarInOutHandle(sentryLogin).adjustCarNum(send_data['carNum'], send_data['adjustCarNum'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarInNumMsg"])

    def test_checkCarIn(self,sentryLogin,send_data,expect):
        """岗亭端登记放行-看校正后进场车辆屏显语音开闸"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['adjustCarNum'],send_data['carInHandleType'],send_data['carIn_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])
        Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarInOpenGate"])

    def test_checkAdjustCarInWaterNum(self,userLogin,send_data,expect):
        """查看校正进场车辆流水"""
        re = Information(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkName'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarInWaterNumMsg"])

    def test_mockCarOut(self,send_data,expect):
        """离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_adjustCarOutNum(self,sentryLogin,send_data,expect):
        """校正出场车辆"""
        re = CarInOutHandle(sentryLogin).adjustCarNum(send_data['carNum'], send_data['adjustCarNum'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarOutNumMsg"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['adjustCarNum'],send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_checkAdjustCarOutWaterNum(self,userLogin,send_data,expect):
        """查看校正出场车辆流水"""
        re = Information(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkName'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarOutWaterNumMsg"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["adjustCarNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])
