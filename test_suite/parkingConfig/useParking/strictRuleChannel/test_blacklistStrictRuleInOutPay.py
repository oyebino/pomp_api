#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/21 10:15
# @Author  : 何涌
# @File    : test_blacklistStrictRuleInOutPay.py

import pytest
import allure
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.parkingManage_service.carTypeManage_service.carTypeConfig import CarType ,ParkBlacklist
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/useParking/strictRuleChannel/blacklistStrictRuleInOutPay.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-收费停车场")
@allure.story('黑名单严进-需缴费严出（岗亭收费处收费放行）')
class TestBlacklistStrictRuleInOutPay(BaseCase):
    """黑名单严进，需缴费严出（岗亭收费处收费放行）"""
    def test_addBlacklistSpecialType(self, userLogin, send_data, expect):
        """新建特殊类型-黑名单"""
        re = CarType(userLogin).createSpecialType(send_data['parkName'], send_data['specialCarType'], send_data['typeName'])
        result = re['status']
        Assertions().assert_text(result, expect["addBlacklistSpecialTypeMsg"])

    def test_createBlacklistCarNum(self, userLogin, send_data, expect):
        """创建黑名单车辆"""
        re = ParkBlacklist(userLogin).addBlacklist(send_data['typeName'], send_data['carNum'])
        result = re
        Assertions().assert_in_text(result, expect["createBlacklistCarNumMsg"])

    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result, expect["mockCarIn"])

    def test_checkCarIn(self,sentryLogin,send_data,expect):
        """岗亭端登记放入"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carInHandleType'],'${mytest.carIn_jobId}')
        result = re
        Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
        Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarInIsOpenGate"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['vipType'],expect["checkPresentCarTypeMsg"])

    def test_mockCarOut(self,send_data,expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNum'],1,send_data['outClientID'])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端收费放出"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_text(result['leaveVipTypeStr'], expect["checkCarleaveVipTypeStrMsg"])
        Assertions().assert_text(result['enterVipTypeStr'], expect["checkenterVipTypeStrMsg"])