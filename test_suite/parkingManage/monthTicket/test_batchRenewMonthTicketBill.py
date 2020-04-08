#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/25 14:29
# @Author  : 叶永彬
# @File    : test_batchRenewMonthTicketBill.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/batchRenewMonthTicketBill.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块")
@allure.story('月票失效-然后批量续费月票')
class TestBatchRenewMonthTicketBill():
    """月票失效，然后批量续费月票，开通后在页面可以查看到导入的月票，车辆进出是月票"""
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

    def test_batchRenewTicketBill(self, userLogin, send_data, expect):
        """批量续费月票"""
        re = MonthTicketBill(userLogin).batchRenewMonthTicketBill(send_data['parkName'], send_data['carNum'])
        result = re['success']
        Assertions().assert_text(result, expect["batchRenewTicketBillMsg"])

    def test_checkMonthTicketBillList(self, userLogin, send_data, expect):
        """查看到续费的月票-已生效"""
        re = MonthTicketBill(userLogin).getMonthTicketBillList(send_data['parkName'], send_data['carNum'], combinedStatus = send_data['combinedStatus'])
        result = re
        Assertions().assert_in_text(result, expect["checkMonthTicketBillListMsg"])

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
        Assertions().assert_in_text(result['screen'], expect["mockCarOutScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["mockCarOutVoiceMsg"])