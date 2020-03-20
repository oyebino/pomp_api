#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/19 16:56
# @Author  : 叶永彬
# @File    : test_editTicketConfigStatus.py

import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.information_service.information import Information
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/editTicketConfigStatus.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestEditTicketConfigStatus():
    """月票创建，属于上架状态，可以售卖，然后操作下架，再执行售卖，发现无法售卖，再执行上架，可以售卖"""
    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建自定义月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'],send_data['renewMethod'], send_data['validTo'])
        result = re.json()
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_setMonthTicketConfigInvalid(self, userLogin, send_data, expect):
        """设置月票类型下架"""
        re = MonthTicketConfig(userLogin).updateStatusMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'],send_data['downTicketStatus'])
        result = re.json()
        Assertions().assert_in_text(result, expect["setMonthTicketConfigInvalidMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自定义月票类型开通月票,不能查到该月票进行开通"""
        re = MonthTicketBill(userLogin).getValidCofigList()
        result = re.json()
        Assertions().assert_not_in_text(result, expect["openMonthTicketBillMsg"])

    def test_setMonthTicketConfigValid(self, userLogin, send_data, expect):
        """设置月票类型上架"""
        re = MonthTicketConfig(userLogin).updateStatusMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'],send_data['upTicketStatus'])
        result = re.json()
        Assertions().assert_in_text(result, expect["setMonthTicketConfigValidMsg"])

    def test_openMonthTicketBillAgain(self, userLogin, send_data, expect):
        """用月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNum'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re.json()
        Assertions().assert_in_text(result, expect["openMonthTicketBillAgainMsg"])

    def test_editMonthTicketBill(self, userLogin, send_data, expect):
        """编辑月票订单"""
        re = MonthTicketBill(userLogin).editOpenMonthTicketBill(send_data['parkName'], send_data['carNum'], send_data['editUser'])
        result = re.json()['status']
        Assertions().assert_text(result, expect["editMonthTicketBillMsg"])

    def test_checkTicketBillUpdateRecord(self, userLogin, send_data, expect):
        """查看月票操作日志是否修改"""
        re = MonthTicketBill(userLogin).getListBillUpdateRecord(send_data['parkName'], send_data['carNum'])
        result = re.json()
        Assertions().assert_in_text(result, expect["checkTicketBillUpdateRecordMsg"])

    def test_editMonthTicketConfig(self, userLogin, send_data, expect):
        """售买后，编辑月票类型"""
        re = MonthTicketConfig(userLogin).editMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'],send_data['newTicketTypeName'])
        result = re.json()['status']
        Assertions().assert_in_text(result, expect["editMonthTicketConfigMsg"])

    def test_checkSystemLog(self, userLogin, send_data, expect):
        """查看系统操作日志-对应的是编辑月票的内容"""
        re = Information(userLogin).getSystemLog(send_data['menuLevel'])
        result = re.json()['data']['rows'][0]
        Assertions().assert_in_text(result['operationObject'], expect["checkSystemLogMsg"])
