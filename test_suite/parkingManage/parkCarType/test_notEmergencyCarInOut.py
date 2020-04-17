#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 9:53
# @Author  : 叶永彬
# @File    : test_notEmergencyCarInOut.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.emergencyCarNum import EmergencyCarNum
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/notEmergencyCarInOut.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
@allure.story('非告警车牌进出场看不到告警记录')
class TestNotEmergencyCarInOut(BaseCase):
    """非告警车牌进出场看不到告警记录"""
    def test_createEmergencyCarConfig(self, userLogin, send_data, expect):
        """创建固定告警车牌"""
        re = EmergencyCarNum(userLogin).createEmergencyCarNum(send_data['parkName'], send_data['oldCarNum'], send_data['tel'])
        result = re
        Assertions().assert_in_text(result, expect["createEmergencyCarConfigMsg"])

    def test_openEmergencySetting(self, userLogin, send_data, expect):
        """开启告警设置"""
        re = EmergencyCarNum(userLogin).updateEmergencySetting()
        result = re
        Assertions().assert_in_text(result, expect["openEmergencySettingMsg"])

    def test_updateEmergencyCarNum(self, userLogin, send_data, expect):
        """修改固定告警车牌"""
        re = EmergencyCarNum(userLogin).updateEmergencyCarNum(send_data['parkName'], send_data['oldCarNum'], send_data['newCarNum'])
        result = re
        Assertions().assert_in_text(result, expect["updateEmergencyCarNumMsg"])

    def test_mockCarIn(self,sentryLogin, send_data, expect):
        """模拟非告警车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["oldCarNum"], 0, send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkEmergencyCarInRecord(self, userLogin, send_data, expect):
        """查看进场车辆告警记录没有该非告警车辆"""
        re = Information(userLogin).getEmergencyCarRecord(send_data['parkName'], send_data['carType'],send_data['oldCarNum'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkEmergencyCarInRecordMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟告警车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["oldCarNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["oldCarNum"],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkEmergencyCarOutRecord(self, userLogin, send_data, expect):
        """查看出场车辆告警记录没有该非告警车辆"""
        re = Information(userLogin).getEmergencyCarRecord(send_data['parkName'], send_data['carType'],send_data['oldCarNum'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkEmergencyCarOutRecordMsg"])

    def test_delEmergencyCarConfig(self, userLogin, send_data, expect):
        """删除固定告警车辆配置"""
        re = EmergencyCarNum(userLogin).delEmergencyCarNum(send_data['parkName'], send_data['newCarNum'])
        result = re
        Assertions().assert_in_text(result, expect["delEmergencyCarConfigMsg"])