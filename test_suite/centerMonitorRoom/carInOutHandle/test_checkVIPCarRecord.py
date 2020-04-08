#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/30 16:46
# @Author  : 叶永彬
# @File    : test_checkVIPCarRecord.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centerMonitorRoom/carInOutHandle/checkVIPCarRecord.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('远程值班室查看VIP车辆')
class TestCheckVIPCarRecord():

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

    def test_checkMonthTicketListRecord(self, centerMonitorLogin, send_data, expect):
        """查看VIP车辆列表记录"""
        re = CarInOutHandle(centerMonitorLogin).checkMonthTicketList(send_data['parkName'], send_data['carNum'],send_data['ticketTypeName'])
        result = re[0]
        Assertions().assert_in_text(result['carCode'], expect["checkMonthTicketListRecordMsg"])