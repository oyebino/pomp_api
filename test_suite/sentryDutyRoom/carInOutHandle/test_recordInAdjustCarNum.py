#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 14:07
# @Author  : 何涌
# @File    : test_recordInAdjustCarNum.py

import pytest,allure
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information
from common.utils import YmlUtils
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/recordInAdjustCarNum.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处进场记录校正')

class TestRecordInAdjustCarNum(BaseCase):

    """岗亭收费处进场记录校正"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_recordIn(self, sentryLogin, send_data, expect):
        """在pc端查看进场记录"""
        re = CarInOutHandle(sentryLogin).getCarInRecord(send_data['carNum'], send_data['parkName'])
        result = re
        Assertions().assert_in_text(result, expect['carNum'])

    def test_adjustCarNum(self, sentryLogin, send_data, expect):
        """在岗亭收费处在场车辆里面校正车牌"""
        re = CarInOutHandle(sentryLogin).patchRecord(send_data['carNum'], send_data['parkName'], send_data['adjustCarNum'])
        result = re
        Assertions().assert_text(result, "")

    def test_checkAdjustCarInWaterNum(self, userLogin, send_data, expect):
        """查看校正进场车辆流水"""
        re = Information(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkName'])
        result = re
        Assertions().assert_in_text(result, expect["adjustCarInWaterNumMsg"])

    def test_recordIn2(self, sentryLogin, send_data, expect):
        """在岗亭收费处在场车辆里面查看校正后车牌"""
        re = CarInOutHandle(sentryLogin).getCarInRecord(send_data['adjustCarNum'], send_data['parkName'])
        result = re
        Assertions().assert_in_text(result, expect['adjustCarNum'])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["adjustCarNum"], 1, send_data["lightRule_outClientID"])
        result = re
        Assertions().assert_in_text(result, expect['mockCarOutMessage'])

    def test_checkOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['adjustCarNum'], send_data['carOutHandleType'])
        result = re
        Assertions().assert_in_text(result, expect["checkOutMessage"])

    def test_recordOut(self, sentryLogin, send_data, expect):

        """在pc端查看离场记录"""
        re = CarInOutHandle(sentryLogin).getCarOutRecord(send_data['adjustCarNum'], send_data['parkName'])
        result = re[0]['carCode']
        Assertions().assert_in_text(result, expect['adjustCarNum'])