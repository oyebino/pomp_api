#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 14:07
# @Author  : 何涌
# @File    : test_recordInAdjustCarNum.py

import allure,os
import pytest

from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/recordInAdjustCarNum.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")

class TestRecordInAdjustCarNum(BaseCase):

    """岗亭收费处进场记录校正"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_recordIn(self, sentryLogin, send_data, expect):
        """在pc端查看进场记录"""
        re = CarInOutHandle(sentryLogin).record_car_in(send_data['carNum'])
        result = re.json()['rows'][0]['carCode']
        Assertions().assert_in_text(result, expect['carNum'])

    def test_adjustCarNum(self, sentryLogin, send_data, expect):
        """在岗亭收费处在场车辆里面校正车牌"""
        CarInOutHandle(sentryLogin).record_car_in_adjust(send_data['carNum'], send_data['adjustCarNum'])
        """该校正接口没有返回值只能通过查校正流水确认"""

    def test_checkAdjustCarInWaterNum(self, userLogin, send_data, expect):
        """查看校正进场车辆流水"""
        re = Information(userLogin).getAdjustCarWaterNum(send_data['adjustCarNum'], send_data['parkId'])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["adjustCarInWaterNumMsg"])

    def test_recordIn2(self, sentryLogin, send_data, expect):
        """在岗亭收费处在场车辆里面查看校正后车牌"""
        re = CarInOutHandle(sentryLogin).record_car_in(send_data['adjustCarNum'])
        result = re.json()['rows'][0]['carCode']
        Assertions().assert_in_text(result, expect['adjustCarNum'])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["adjustCarNum"], 1, send_data["lightRule_outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect['mockCarOutMessage'])

    def test_checkOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).normal_car_out(send_data['adjustCarNum'])
        result = re.json()["success"]
        Assertions().assert_in_text(result, expect["checkOutMessage"])

    def test_recordOut(self, sentryLogin, send_data, expect):

        """在pc端查看离场记录"""
        re = CarInOutHandle(sentryLogin).record_car_out(send_data['adjustCarNum'])
        result = re.json()['rows'][0]['carCode']
        Assertions().assert_in_text(result, expect['adjustCarNum'])