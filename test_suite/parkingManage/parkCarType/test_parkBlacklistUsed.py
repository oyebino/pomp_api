#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 15:11
# @Author  : 叶永彬
# @File    : test_parkBlacklistUsed.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import CarType ,ParkBlacklist
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/parkBlacklistUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
@allure.story('黑名单车辆新增、修改、使用流程')
class TestParkBlacklistUsed(BaseCase):
    """黑名单车辆新增、修改、使用流程"""
    def test_addBlacklistSpecialType(self, userLogin, send_data, expect):
        """新建特殊类型-黑名单"""
        re = CarType(userLogin).createSpecialType(send_data['parkName'], send_data['specialCarType'], send_data['typeName'])
        result = re['status']
        Assertions().assert_text(result, expect["addBlacklistSpecialTypeMsg"])

    def test_editBlacklistSpecialType(self, userLogin, send_data, expect):
        """修改特殊类型-黑名单"""
        re = CarType(userLogin).updataSpecialCarTypeConfig(send_data['typeName'], send_data['newTypeName'])
        result = re['status']
        Assertions().assert_text(result, expect["editBlacklistSpecialTypeMsg"])

    def test_createBlacklistCarNum(self, userLogin, send_data, expect):
        """创建黑名单车辆"""
        re = ParkBlacklist(userLogin).addBlacklist(send_data['newTypeName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["createBlacklistCarNumMsg"])

    def test_mockCarIn(self, send_data, expect):
        """模拟黑名单车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkPresentCarType(self, userLogin, send_data, expect):
        """查看黑名单车在场类型"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['vipType'], expect["checkPresentCarTypeMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟黑名单车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNum"],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkCarLeaveType(self, userLogin, send_data, expect):
        """查看黑名单车辆离场记录车辆类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data['parkName'], send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['leaveVipTypeStr'], expect["checkCarleaveVipTypeStrMsg"])
        Assertions().assert_text(result['enterVipTypeStr'], expect["checkenterVipTypeStrMsg"])

    def test_delBlacklistCarNum(self, userLogin, send_data, expect):
        """删除黑名单车辆-黑名单车录入"""
        re = ParkBlacklist(userLogin).delBlacklist(send_data['parkName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["delBlacklistCarNumMsg"])

    def test_checkDelBlacklistCarNum(self, userLogin, send_data, expect):
        """查看已删除黑名单车辆是否存在"""
        re = ParkBlacklist(userLogin).getBlacklist(send_data['parkName'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkDelBlacklistCarNumMsg"])