#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 16:59
# @Author  : 叶永彬
# @File    : test_sendVoiceMsg.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centerMonitorRoom/carInOutHandle/sendVoiceMsg.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('远程值班室发送语音消息')
class TestSendVoiceMsg():

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self, centerMonitorLogin, send_data,expect):
        """模拟离场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sendVoiceMsg(self, centerMonitorLogin, send_data,expect):
        """发送语音"""
        re = CarInOutHandle(centerMonitorLogin).sendVoiceMessage(send_data["carNum"], send_data['voiceMsg'])
        result = re['status']
        Assertions().assert_text(result, expect["sendVoiceMsg"])

    def test_checkCarMsgYtj(self,send_data,expect):
        """查看一体机语音信息"""
        re = cloudparking_service().getCarMsgYtj(send_data['carOut_jobId'])
        result = re
        Assertions().assert_text(result['screen'], expect["YtjScreen"])
        Assertions().assert_text(result['voice'], expect["YtjVoice"])

    def test_dutyRoomCheckCarOut(self, centerMonitorLogin, send_data, expect):
        """值班室异常放行车辆"""
        re = CarInOutHandle(centerMonitorLogin).checkCarOut(send_data['carNum'])
        result = re['status']
        Assertions().assert_text(result, expect["dutyRoomCheckCarOutMsg"])
