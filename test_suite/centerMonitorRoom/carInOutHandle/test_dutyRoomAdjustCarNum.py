#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/1 13:46
# @Author  : 叶永彬
# @File    : test_dutyRoomAdjustCarNum.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centerMonitorRoom/carInOutHandle/dutyRoomAdjustCarNum.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('远程值班室车辆严进校正车牌')
class TestDutyRoomAdjustCarNum(BaseCase):

    def test_mockCarIn(self,centerMonitorLogin, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMsg"])

    def test_dutyRoomAdjustCarNum(self,centerMonitorLogin, send_data, expect):
        """校正车牌"""
        re = CarInOutHandle(centerMonitorLogin).adjustCarNum(send_data['carNum'], send_data['correctCarNum'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarNumMsg"])

    def test_dutyRoomCheckCarIn(self, centerMonitorLogin, send_data, expect):
        """值班室登记放行车辆"""
        re = CarInOutHandle(centerMonitorLogin).checkCarIn(send_data['correctCarNum'])
        result = re['status']
        Assertions().assert_text(result, expect["dutyRoomCheckCarInMsg"])

    def test_cendutyCarInRecord(self, centerMonitorLogin, send_data, expect):
        """查看远程值班室进场记录"""
        re = CarInOutHandle(centerMonitorLogin).carInOutRecord(send_data['parkName'], send_data['correctCarNum'], 'in')
        result = re[0]
        Assertions().assert_text(result['carCode'], expect["checkCarInRecordMsg"])

