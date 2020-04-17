#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/07 14:35
# @Author  : 何涌
# @File    : test_monthTicketFullPositionStrictInVipCharge.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.cloudparking_service import cloudparking_service
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/monthTicketFullPositionControl/monthTicketFullPositionStrictInVipCharge.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块-VIP类型满位限行")
@allure.story('系统有空位自动放行，无空位手动放行按VIP计费')
class TestMonthTicketFullPositionStrictInVipCharge(BaseCase):
    """VIP类型满位限行（系统有空位自动放行，无空位手动放行按VIP计费）"""

    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建满位控制月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'],openVipFullLimit=send_data['openVipFullLimit'])
        result = re
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用满位控制月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNumList'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    # 满位VIP第一辆车进车
    def test_mockCarInA(self, sentryLogin, send_data, expect):
        """模拟车辆A进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["inscreenAMsg"])
        Assertions().assert_in_text(result['voice'], expect["invoiceAMsg"])

    def test_presentCarA(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarAMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarAvipTypeMsg"])

    # 满位VIP第二辆车进车
    def test_mockCarInB(self, send_data, expect):
        """模拟车辆B进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],0,send_data["inClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["inscreenB"])
        Assertions().assert_in_text(result['voice'], expect["invoiceB"])

    def test_sentryCheckIn(self, sentryLogin, send_data, expect):
        """车辆B登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNumB'],send_data['carInHandleType'],'${mytest.carIn_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect["sentryCheckInMsg"])

    def test_presentCarB(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarBMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarBvipTypeBMsg"])

    # 满位VIP第一辆车出车
    def test_mockCarOutA(self, send_data, expect):
        """模拟车辆A离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["outScreenA"])
        Assertions().assert_in_text(result['voice'], expect["outVoiceA"])

    def test_carLeaveHistoryA(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carAInOutVipTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carAInOutVipTypeMsg"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOutB(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],1,send_data["outClientID"])
        result = re
        Assertions().assert_in_text(result['screen'], expect["outscreenB"])
        Assertions().assert_in_text(result['voice'], expect["outvoiceB"])

    def test_carLeaveHistoryB(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carInOutVipTypeStrMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carInOutVipTypeStrMsg"])