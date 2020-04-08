#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/25 16:25
# @Author  : 何涌
# @File    : test_checkHistoryMsg.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/checkHistoryMsg.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处查看历史消息')
@pytest.mark.skip(reason='尚未处理')
class TestCheckHistoryMsg(BaseCase):
    """岗亭收费处查看历史消息"""
    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_checkCarIn(self,sentryLogin,send_data,expect):
        """岗亭端登记放入"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carInHandleType'],send_data['carIn_jobId'])
        result = re
        Assertions().assert_in_text(result, expect["checkCarInMessage"])

    def test_checkOneHistoryMsg(self,sentryLogin,send_data,expect):
        """岗亭端查看单条记录的历史消息详情"""
        re = CarInOutHandle(sentryLogin).check_history_msg(send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result["content"]["carNo"], expect["checkOneHistoryMsgCarNo"])
        Assertions().assert_in_text(result["content"]["reason"], expect["checkOneHistoryMsgReason"])
        Assertions().assert_in_text(result["content"]["abName"], expect["checkOneHistoryMsgAbName"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkCarOut(self,sentryLogin,send_data,expect):
        """岗亭端收费放出"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result, expect["checkCarOutMessage"])

    def test_checkOneHistoryMsg2(self,sentryLogin,send_data,expect):
        """岗亭端查看单条记录的历史消息详情"""
        re = CarInOutHandle(sentryLogin).check_history_msg(send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result["content"]["leaveCarNo"], expect["checkOneHistoryMsgCarNo2"])
        Assertions().assert_in_text(result["content"]["reason"], expect["checkOneHistoryMsgReason2"])
        Assertions().assert_in_text(result["content"]["abName"], expect["checkOneHistoryMsgAbName2"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"],send_data["carNum"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])