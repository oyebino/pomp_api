#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 11:24
# @Author  : 叶永彬
# @File    : test_operatorOnLineStatus.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.personalInfo import PersonalInfo
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centerMonitorRoom/personalInfo/operatorOnLineStatus.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('操作员下班-离开状态')
class TestOperatorOnLineStatus(BaseCase):

    def test_operatorStatusLeave(self, centerMonitorLogin, send_data, expect):
        """当班状态离开"""
        re = PersonalInfo(centerMonitorLogin).cendutySeatChangeStatus(send_data['leaveStatus'])
        result = re['message']
        Assertions().assert_text(result, expect['operatorStatusLeaveMsg'])

    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场-严进"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_getCarInHandleInfo(self, send_data, expect):
        """"下班状态不能-获取车辆处理信息"""
        re = cloudparking_service().getCenterMonitorMsgList()
        result = re.json()
        Assertions().assert_not_in_text(result, expect["getCarInHandleMsg"])

    def test_operatorStatusOn(self, centerMonitorLogin, send_data, expect):
        """上班"""
        re = PersonalInfo(centerMonitorLogin).cendutySeatChangeStatus(send_data['onStatus'])
        result = re['message']
        Assertions().assert_text(result, expect['operatorStatusOnMsg'])

    def test_operatorStatusOff(self, centerMonitorLogin, send_data, expect):
        """下班"""
        re = PersonalInfo(centerMonitorLogin).cendutySeatChangeStatus(send_data['offStatus'])
        result = re['message']
        Assertions().assert_text(result, expect['operatorStatusOffMsg'])