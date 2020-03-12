#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12 11:29
# @Author  : 叶永彬
# @File    : test_emergencyCarY.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.parkingManage_service.carTypeManage_service.emergencyCarNum import EmergencyCarNum
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/parkCarType/emergencyCarY.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆分类管理")
class TestEmergencyCarY(BaseCase):
    """指定告警粤Y类车牌新增-修改-使用流程"""
    def test_createEmergencyCarConfig(self, userLogin, send_data, expect):
        """创建告警车牌"""
        re = EmergencyCarNum(userLogin).createEmergencyCarNum(send_data['parkName'], send_data['oldEmergencyCarNum'], send_data['tel'])
        result = re.json()
        Assertions().assert_in_text(result, expect["createEmergencyCarConfigMsg"])

    def test_openEmergencySetting(self, userLogin, send_data, expect):
        """开启告警设置"""
        re = EmergencyCarNum(userLogin).updateEmergencySetting()
        result = re.json()
        Assertions().assert_in_text(result, expect["openEmergencySettingMsg"])

    def test_updateEmergencyCarNum(self, userLogin, send_data, expect):
        """修改告警车牌"""
        re = EmergencyCarNum(userLogin).updateEmergencyCarNum(send_data['parkName'], send_data['oldEmergencyCarNum'], send_data['newEmergencyCarNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["updateEmergencyCarNumMsg"])

    def test_mockCarIn(self, send_data, expect):
        """模拟告警车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkEmergencyCarInRecord(self, userLogin, send_data, expect):
        """查看告警进场车辆记录"""
        re = Information(userLogin).getEmergencyCarRecord(send_data['parkName'], send_data['carType'],send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkEmergencyCarInRecordMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟告警车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNum"],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re.json()
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkEmergencyCarOutRecord(self, userLogin, send_data, expect):
        """查看告警进场车辆记录"""
        re = Information(userLogin).getEmergencyCarRecord(send_data['parkName'], send_data['carType'],send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkEmergencyCarOutRecordMsg"])

    def test_delEmergencyCarConfig(self, userLogin, send_data, expect):
        """删除告警车辆配置"""
        re = EmergencyCarNum(userLogin).delEmergencyCarNum(send_data['parkName'], send_data['newEmergencyCarNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["delEmergencyCarConfigMsg"])