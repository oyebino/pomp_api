#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/12 14:35
# @Author  : 何涌
# @File    : test_needChargeVipWideInOutProcess.py

import pytest,allure
from common.utils import YmlUtils
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.sentry_service.carInOutHandle import CarInOutHandle

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/needChargeVipWideInOutProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestNeedChargeVipWideInOutProcess():
    """绑定计费组月票车宽进，需缴费宽出"""

    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建绑定计费组月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'],send_data['isChargeGroupRelated'],send_data['vipGroupName'])
        result = re.json()
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用绑定计费组月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNum'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re.json()
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json( )['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["inScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["inVoiceMsg"])

    def test_mockCarOut(self,send_data, expect):
        """模拟车辆出场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["OutScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["OutVoiceMsg"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_checkParkingBillDetail(self, userLogin, send_data, expect):
        """查询收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data['parkName'], send_data['carNum'])
        result = re.json()['data']["rows"][0]
        Assertions().assert_in_text(result['parkVipTypeStr'], expect['checkParkingBillDetailMsg'])

    def test_checkCarInOutHistoryVIPType(self,userLogin,send_data,expect):
        """查看进出场记录中查看到VIP类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re.json()["data"]["rows"][0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
