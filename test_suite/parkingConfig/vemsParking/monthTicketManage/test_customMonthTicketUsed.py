#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/22 14:24
# @Author  : 叶永彬
# @File    : test_customMonthTicketUsed.py

import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.offLineParking_service.vemsParkingReq import VemsParkingReq

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/vemsParking/monthTicketManage/customMonthTicketUsed.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("线下车场-月票管理模块")
@allure.story('vems自定义月票创建创建并使用')
class TestCustomMonthTicketUsed():
    """VEMS车场自定义月票创建，开通，续费。车辆进出是月票（在进出场记录中查看到VIP类型为售卖的月票类型）"""
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

    def test_ticketBillResync(self, userLogin, send_data, expect):
        """月票订单重新同步"""
        re = MonthTicketBill(userLogin).resyncMonthTicketBill(send_data['parkName'], send_data['carNum'])
        result = re
        Assertions().assert_text(result['status'], expect["ticketBillResyncMsg"])

    def test_mockCarIn(self,openYDTLogin,send_data,expect):
        """模拟车辆进场"""
        re = VemsParkingReq(openYDTLogin).carInOut(send_data['parkCode'],send_data["carNum"],0)
        result = re
        Assertions().assert_text(result['message'], expect["mockCarInMsg"])

    def test_mockCarOut(self,openYDTLogin,send_data, expect):
        """模拟车辆出场"""
        re = VemsParkingReq(openYDTLogin).carInOut(send_data['parkCode'],send_data["carNum"],1)
        result = re
        Assertions().assert_text(result['message'], expect["mockCarOutMsg"])

    def test_checkCarInOutHistoryVIPType(self,userLogin,send_data,expect):
        """查看进出场记录中查看到VIP类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
