#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/24 15:45
# @Author  : 何涌
# @File    : test_noPresenceVipStrictOutProcess.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/noPresenceVipStrictOutProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块")
@allure.story('VIP车无在场严出')
class TestNoPresenceVipStrictOutProcess():
    """VIP车无在场严出"""
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

    def test_mockCarOut(self,sentryLogin, send_data, expect):
        """模拟月票车无在场辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['open_gate'], expect["outOpenGateMsg"])
        Assertions().assert_in_text(result['screen'], expect["outScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["outVoiceMsg"])

    def test_checkMessageOut(self, sentryLogin, send_data, expect):
        """岗亭端登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["checkMessageOutMsg"])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNum"])
        result = re[0]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMsg"])




