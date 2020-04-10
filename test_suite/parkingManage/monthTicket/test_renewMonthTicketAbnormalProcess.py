#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 14:35
# @Author  : 何涌
# @File    : test_renewMonthTicketAbnormalProcess.py

import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/renewMonthTicketAbnormalProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块")
@allure.story('月票过期-续费(续费日期不包含当前时间)-车辆进出就临时车')
class TestRenewMonthTicketAbnormalProcess():
    """月票过期，车辆进出，不是月票，然后执行月票续费（续费日期不包含当前时间），车辆进出，不是月票"""

    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建自定义月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'])
        result = re
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自定义月票类型开通月票-已过期"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNum'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["mockCarInScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockCarInVoiceMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["mockCarOutScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockCarOutVoiceMsg"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_renewMonthTicketBill(self, userLogin, send_data, expect):
        """月票续费-不在当前时间（未来时间）"""
        re = MonthTicketBill(userLogin).renewMonthTicketBill(send_data['parkName'], send_data['carNum'], send_data['status'], send_data['renewDate'])
        result = re
        Assertions().assert_in_text(result, expect["renewMonthTicketBillMsg"])

    def test_mockMonthTicketCarIn(self,send_data,expect):
        """模拟月票车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["mockTicketCarInScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockTicketCarInVoiceMsg"])

    def test_mockMonthTicketCarOut(self, send_data, expect):
        """模拟月票车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["mockTicketCarOutScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockTicketCarOutVoiceMsg"])

    def test_sentryPayAgain(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_checkCarInOutHistoryVIPType(self,userLogin,send_data,expect):
        """查看进出场记录中查看到VIP类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])

