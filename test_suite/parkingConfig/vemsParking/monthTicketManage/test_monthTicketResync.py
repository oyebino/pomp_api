#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/23 9:17
# @Author  : 叶永彬
# @File    : test_monthTicketResync.py
import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from common.BaseCase import BaseCase
from common.Assert import Assertions
from Api.offLineParking_service.vemsParkingReq import VemsParkingReq

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/vemsParking/monthTicketManage/monthTicketResync.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("线下车场-月票管理模块")
@allure.story('vems月票订单及类型同步')
class TestMonthTicketResync(BaseCase):
    """VEMS月票类型以及修改月票订单同步"""
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
        re = MonthTicketBill(userLogin).renewMonthTicketBill(send_data['parkName'], send_data['carNum'], send_data['status'],send_data['startData'])
        result = re
        Assertions().assert_in_text(result, expect["renewMonthTicketBillMsg"])

    def test_ticketBillResync(self, userLogin, send_data, expect):
        """月票订单重新同步"""
        re = MonthTicketBill(userLogin).resyncMonthTicketBill(send_data['parkName'], send_data['carNum'],send_data['combinedStatus'])
        result = re
        Assertions().assert_text(result['status'], expect["ticketBillResyncMsg"])

    def test_checkVemsEditMonthBillInfo(self, openYDTLogin, send_data, expect):
        """查看修改后月票订单的信息"""
        re = VemsParkingReq(openYDTLogin).getMonthCard(send_data['parkCode'],send_data['carNum'])
        result = re[0]
        self.save_data("vemsTicketName",result['monthCardName'])
        Assertions().assert_in_text(result, expect["checkVemsEditMonthBillInfo"])

    def test_checkVemsTicketType(self,openYDTLogin, send_data, expect):
        """查看Vems同步后月票类型"""
        re = VemsParkingReq(openYDTLogin).getVipType(send_data['parkCode'], send_data['customVipName'])
        result = re[0]
        Assertions().assert_in_text(result, expect["checkVemsTicketType"])