#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 14:13
# @Author  : 叶永彬
# @File    : test_yellowCarWideInOut.py

import pytest,allure
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/yellowCarWideInOut.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('黄牌车宽进-需缴费宽出（岗亭收费处收费放行）')
class TestYellowCarWideInOut(BaseCase):
    """黄牌车宽进，需缴费宽出（岗亭收费处收费放行）"""
    def test_mockCarIn(self,sentryLogin, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"], carType = send_data['carType'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMsg"])

    def test_presentCarType(self,userLogin, send_data, expect):
        """查看在场车辆"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['enterCarType'], expect["presentCarTypeMsg"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPaty(self, sentryLogin, send_data, expect):
        """岗亭端收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])