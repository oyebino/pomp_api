#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 15:16
# @Author  : 叶永彬
# @File    : test_parkWhitelistUsed.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import ParkWhitelist
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/parkWhitelistUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
class TestParkWhitelistUsed(BaseCase):
    """白名单车辆新增、修改、使用流程"""
    def test_createWhitelistCar(self, userLogin, send_data, expect):
        """创建白名单车辆"""
        re = ParkWhitelist(userLogin).addWhitelist(send_data['parkName'], send_data['carNum'])
        result = re.json()['status']
        Assertions().assert_text(result, expect["createWhitelistCarMsg"])

    def test_mockCarIn(self, send_data, expect):
        """模拟白名单车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkPresentCarType(self, userLogin, send_data, expect):
        """查看白名单车辆在场类型"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNum'])
        result = re.json()['data']['rows'][0]['vipType']
        Assertions().assert_text(result, expect["checkPresentCarTypeMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟白名单车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarLeaveType(self, userLogin, send_data, expect):
        """查看白名单车辆离场记录车辆类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data['parkName'], send_data['carNum'])
        result = re.json()['data']['rows'][0]
        Assertions().assert_text(result['leaveVipTypeStr'], expect["checkCarleaveVipTypeStrMsg"])
        Assertions().assert_text(result['enterVipTypeStr'], expect["checkenterVipTypeStrMsg"])

    def test_delWhitelistCar(self, userLogin, send_data, expect):
        """删除白名单车辆规则-白名单录入"""
        re = ParkWhitelist(userLogin).delWhilelist(send_data['carNum'])
        result = re.json()['status']
        Assertions().assert_text(result, expect["delWhitelistCarMsg"])

    def test_checkDelWhitelistCar(self, userLogin, send_data, expect):
        """检查已删除白名单不存在"""
        re = ParkWhitelist(userLogin).getWhilelistRuleList()
        result = re.json()
        Assertions().assert_not_in_text(result, expect["checkDelWhitelistCar"])