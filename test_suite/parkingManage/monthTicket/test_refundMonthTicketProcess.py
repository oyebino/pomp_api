#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 14:35
# @Author  : 何涌
# @File    : test_refundMonthTicketProcess.py

import pytest,allure
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/refundMonthTicketProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestRefundMonthTicketProcess():
    """车辆开通月票，车辆进出，是月票，然后执行月票退款，车辆进出，不是月票"""

    # 月票类型创建
    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建自定义月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'])
        result = re.json()
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    # 开通月票
    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自定义月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNum'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re.json()
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    # 开通月票后进车
    def test_mockCarIn(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["inScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["inVoiceMsg"])

    # 开通月票后出车
    def test_mockCarOut(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["OutScreenMsg"])
        Assertions().assert_in_text(result['voice'], expect["OutVoiceMsg"])

    def test_CarLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNum"])
        result = re.json()["data"]["rows"][0]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])

    # 月票退款
    def test_refundMonthTicket(self,userLogin,send_data,expect):
        re = MonthTicketBill(userLogin).refundMonthTicketBill(send_data["parkName"], send_data["carNum"], send_data['refundValue'])
        result = re.json()
        Assertions().assert_in_text(result,expect["refundMonthTicketMsg"])

    # 月票退款后进车
    def test_mockCarIn2(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["inscreen2"])
        Assertions().assert_in_text(result['voice'], expect["invoice2"])

    # 月票退款后出车
    def test_mockCarOut2(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["outscreen2"])
        Assertions().assert_in_text(result['voice'], expect["outvoice2"])

    def test_sentryPay(self, sentryLogin, send_data, expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_checkCarInOutHistoryVIPType(self,userLogin,send_data,expect):
        """查看进出场记录中查看到VIP类型"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNum"])
        result = re.json()["data"]["rows"][0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["checkCarInOutHistoryVIPTypeMsg"])

