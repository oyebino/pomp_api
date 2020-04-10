#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 14:44
# @Author  : 叶永彬
# @File    : test_checkTollFlow.py

import allure,pytest
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.sentry_service.personalInfo import PersonalInfo
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/checkTollFlow.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处查看收费流水')
class TestCheckTollFlow(BaseCase):
    """岗亭收费处查看收费流水"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect['mockCarOutMessage'])

    def test_sentryPay(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carOutHandleType'], '${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_offDuty(self, sentryLogin, send_data, expect):
        """下班"""
        re = PersonalInfo(sentryLogin).offduty()
        result = re
        Assertions().assert_text(result, '')

    def test_shiftMoneys(self, sentryLogin, send_data, expect):
        """查看收费流水清单"""
        re = PersonalInfo(sentryLogin).shiftMoneys()
        result = re[0]
        Assertions().assert_text(result['car_code'], expect['tollFlowCarCodeMsg'])
        Assertions().assert_in_text(result['payVal'], expect['tollFlowPayValMsg'])