#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 9:48
# @Author  : 叶永彬
# @File    : test_carOutNoInside.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information_controller import Information_controller
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOut_service.checkInOut_service import CheckInOut
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/carInOut_service/carOutNoInside.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("车辆进出模块")
class TestCarOutNoInside(BaseCase):
    """临时车无在场需缴费宽出（岗亭收费处收费放行）"""
    def test_mockCarOut(self, send_data, expect):
        """离场"""
        re = cloudparking_service().mock_car_in_out(send_data['carNum'], 1, send_data['outClientID'])
        result = re.json()
        self.save_data('carOut_jobId', result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryAbnormalPay(self,sentryLogin,send_data,expect):
        """岗亭端收费异常放行"""
        re = CheckInOut(sentryLogin).abnormal_car_out(send_data['parkUUID'])
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_checkCarOutInfo(self,send_data,expect):
        """查看车辆离场ytj信息"""
        re = cloudparking_service().get_car_msg_ytj(send_data['carOut_jobId'])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])