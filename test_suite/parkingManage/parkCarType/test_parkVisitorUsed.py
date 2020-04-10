#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 15:11
# @Author  : 叶永彬
# @File    : test_parkVisitorUsed.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import CarType ,ParkVisitor
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/parkVisitorUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
@allure.story('访客车辆新增、修改、使用流程')
class TestParkVisitorUsed(BaseCase):
    """访客车辆新增、修改、使用流程"""
    def test_addVisitorSpecialType(self, userLogin, send_data, expect):
        """新建特殊类型-访客"""
        re = CarType(userLogin).createSpecialType(send_data['parkName'], send_data['specialCarType'], send_data['typeName'])
        result = re['status']
        Assertions().assert_text(result, expect["addVisitorSpecialTypeMsg"])

    def test_editVisitorSpecialType(self, userLogin, send_data, expect):
        """修改特殊类型-访客"""
        re = CarType(userLogin).updataSpecialCarTypeConfig(send_data['typeName'], send_data['newTypeName'])
        result = re['status']
        Assertions().assert_text(result, expect["editVisitorSpecialTypeMsg"])

    def test_createVisitorCarNum(self, userLogin, send_data, expect):
        """创建访客车辆"""
        re = ParkVisitor(userLogin).addVisitor(send_data['newTypeName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["createVisitorCarNumMsg"])

    def test_mockCarIn(self, send_data, expect):
        """模拟访客车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkPresentCarType(self, userLogin, send_data, expect):
        """查看访客车在场类型"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['vipType'], expect["checkPresentCarTypeMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟访客车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNum"],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkCarLeaveType(self, userLogin, send_data, expect):
        """查看访客车辆离场记录车辆类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data['parkName'], send_data['carNum'])
        result = re[0]
        Assertions().assert_text(result['leaveVipTypeStr'], expect["checkCarleaveVipTypeStrMsg"])
        Assertions().assert_text(result['enterVipTypeStr'], expect["checkenterVipTypeStrMsg"])

    def test_delVisitorCarNum(self, userLogin, send_data, expect):
        """删除访客车辆-访客车录入"""
        re = ParkVisitor(userLogin).delVisitor(send_data['parkName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["delVisitorCarNumMsg"])

    def test_checkDelVisitorCarNum(self, userLogin, send_data, expect):
        """查看已删除访客车辆是否存在"""
        re = ParkVisitor(userLogin).getParkVisitorList(send_data['parkName'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkDelVisitorCarNumMsg"])
