#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 15:31
# @Author  : 叶永彬
# @File    : test_adjustCarNumByConfidence.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingConfig_service.alarmSetting import AlarmSetting
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/settingParking/alarmSetting/adjustCarNumByConfidence.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-配置停车场-告警配置")
@allure.story('置信度提醒告警配置-远程值班收到并校正车牌')
class TestAdjustCarNumByConfidence(BaseCase):
    """远程值班室收到置信度提醒-并校正车牌"""
    def test_enableConfidenceAlarm(self,userLogin,send_data,expect):
        """开启告警配置-置信度告警功能"""
        re = AlarmSetting(userLogin).setAlarm(send_data['parkName'], send_data['enterConfidence'])
        result = re['status']
        Assertions().assert_text(result, expect['enableConfidenceAlarm'])

    def test_mockCarIn(self,centerMonitorLogin, send_data,expect):
        """模拟进场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data['carNum'],0,send_data['inClientID'], confidence= send_data['carInConfidence'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_adjustCarNumByConfidenceAlarm(self,centerMonitorLogin, send_data,expect):
        """置信度告警-校正车牌"""
        re = CarInOutHandle(centerMonitorLogin).adjustCarNumByConfidenceAlarm(send_data['carNum'], send_data['correctCarNum'])
        result = re['status']
        Assertions().assert_text(result, expect["adjustCarNumByConfidenceAlarmMsg"])

    def test_cendutyCarInRecord(self, centerMonitorLogin, send_data, expect):
        """查看远程值班室进场记录"""
        re = CarInOutHandle(centerMonitorLogin).carInOutRecord(send_data['parkName'], send_data['correctCarNum'], 'in')
        result = re[0]
        Assertions().assert_text(result['carCode'], expect["checkCarInRecordMsg"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["correctCarNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_disableConfidenceAlarm(self,userLogin,send_data,expect):
        """关闭告警配置-置信度告警功能"""
        re = AlarmSetting(userLogin).setAlarm(send_data['parkName'], "")
        result = re['status']
        Assertions().assert_text(result, expect['disableConfidenceAlarm'])
