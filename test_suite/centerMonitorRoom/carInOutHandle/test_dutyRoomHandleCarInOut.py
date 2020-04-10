#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 14:25
# @Author  : 叶永彬
# @File    : test_dutyRoomHandleCarInOut.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centerMonitorRoom/carInOutHandle/dutyRoomHandleCarInOut.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('远程值班室处理进场消息')
class TestDutyRoomHandleCarInOut(BaseCase):
    def test_mockCarIn(self,centerMonitorLogin, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_dutyRoomCheckCarIn(self, centerMonitorLogin, send_data, expect):
        """值班室登记放行车辆"""
        re = CarInOutHandle(centerMonitorLogin).checkCarIn(send_data['carNum'])
        result = re['status']
        Assertions().assert_text(result, expect["dutyRoomCheckCarInMsg"])

    def test_cendutyCarInRecord(self, centerMonitorLogin, send_data, expect):
        """查看远程值班室进场记录"""
        re = CarInOutHandle(centerMonitorLogin).carInOutRecord(send_data['parkName'], send_data['carNum'], 'in')
        result = re[0]
        Assertions().assert_text(result['carCode'], expect["checkCarInRecordMsg"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,centerMonitorLogin, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_dutyRoomCheckCarOut(self, centerMonitorLogin, send_data, expect):
        """值班室异常放行车辆"""
        re = CarInOutHandle(centerMonitorLogin).checkCarOut(send_data['carNum'])
        result = re['status']
        Assertions().assert_text(result, expect["dutyRoomCheckCarOutMsg"])

    def test_cendutyCarOutRecord(self, centerMonitorLogin, send_data, expect):
        """查看远程值班室出场记录"""
        re = CarInOutHandle(centerMonitorLogin).carInOutRecord(send_data['parkName'], send_data['carNum'], 'out')
        result = re[0]
        Assertions().assert_text(result['carCode'], expect["checkCarOutRecordMsg"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """获取出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_text(result['checkOutTypeStr'], expect["carLeaveTypeHistoryMsg"])
        Assertions().assert_text(result['billValue'], expect["carLeaveBillValueHistoryMsg"])
