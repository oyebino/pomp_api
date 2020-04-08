#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/19 10:04
# @Author  : 叶永彬
# @File    : test_customMonthTicketConfigRenew.py

import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/customMonthTicketConfigRenew.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块")
@allure.story('智泊云自定义月票创建创建并使用')
class TestCustomMonthTicketConfig():
    """智泊云自定义月票创建，开通，续费。车辆进出是月票（在进出场记录中查看到VIP类型为售卖的月票类型）"""
    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建自定义月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'])
        result = re
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自定义月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNum'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    def test_renewMonthTicketBill(self, userLogin, send_data, expect):
        """月票续约"""
        re = MonthTicketBill(userLogin).renewMonthTicketBill(send_data['parkName'], send_data['carNum'], send_data['status'])
        result = re
        Assertions().assert_in_text(result, expect["renewMonthTicketBillMsg"])

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["mockCarInScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockCarInVoiceMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result, expect["mockCarOutScreenMsg"])
        Assertions().assert_in_text(result, expect["mockCarOutVoiceMsg"])

    def test_checkCarInOutHistoryVIPType(self,userLogin,send_data,expect):
        """查看进出场记录中查看到VIP类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])