#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/06 14:35
# @Author  : 何涌
# @File    : test_oneParkingSpaceTwoCarWideInInChangeVipProcess.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.monthTicket_service.monthTicketBill import MonthTicketBill
from Api.parkingManage_service.monthTicket_service.monthTicketConfig import MonthTicketConfig
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/oneParkingSpaceTwoCar/oneParkingSpaceTwoCarWideInInChangeVipProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-月票管理模块-一位两车")
@allure.story('第一辆VIP车比第二辆车先离场（开启在场转VIP）')
class TestOneParkingSpaceTwoCarWideInInChangeVipProcess():
    """多位多车VIP转临时车宽进"""
    """一位两车VIP进出场流程，第一辆VIP车比第二辆车先离场（开启在场转VIP）"""

    def test_createMonthTicketConfig(self, userLogin, send_data, expect):
        """创建多位多车月票类型"""
        re = MonthTicketConfig(userLogin).createMonthTicketConfig(send_data['parkName'], send_data['ticketTypeName'], send_data['renewMethod'], send_data['validTo'],isDynamicMode=send_data['isDynamicMode'],autoSwitchVip=send_data['autoSwitchVip'])
        result = re
        Assertions().assert_in_text(result, expect["createMonthTicketConfigMsg"])

    def test_openMonthTicketBill(self, userLogin, send_data, expect):
        """用自定义月票类型开通月票"""
        re = MonthTicketBill(userLogin).openMonthTicketBill(send_data['carNumList'], send_data['ticketTypeName'], send_data['timeperiodListStr'])
        result = re
        Assertions().assert_in_text(result, expect["openMonthTicketBillMsg"])

    # 多位多车VIP第一辆车进车
    def test_mockCarAIn(self, send_data, expect):
        """模拟车辆A进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["inscreenAMsg"])
        Assertions().assert_in_text(result['voice'], expect["invoiceAMsg"])

    def test_presentCarA(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarAMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarAvipTypeMsg"])

    # 多位多车VIP第二辆车进车
    def test_mockCarBIn(self, send_data, expect):
        """模拟车辆B进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],0,send_data["inClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["inscreenB"])
        Assertions().assert_in_text(result['voice'], expect["invoiceB"])

    def test_presentCarB(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['carNo'], expect["presentCarBMsg"])
        Assertions().assert_in_text(result['vipType'], expect["presentCarBvipTypeBMsg"])

    # 多位多车VIP第一辆车出车
    def test_mockCarAOut(self, send_data, expect):
        """模拟车辆A离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],1,send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["outScreenA"])
        Assertions().assert_in_text(result['voice'], expect["outVoiceA"])

    def test_carALeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录A"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumA"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carAInOutVipTypeMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carAInOutVipTypeMsg"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOutB(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],1,send_data["outClientID"])
        result = re.json()['biz_content']['result']
        Assertions().assert_in_text(result['screen'], expect["outscreenB"])
        Assertions().assert_in_text(result['voice'], expect["outvoiceB"])

    def test_sentryPay(self, sentryLogin, send_data, expect):
        """岗亭收费处收费-查看车辆离场信息"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNumB'], send_data['carOutHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result['screen'], expect['sentryPayMsg'])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result,expect["parkingBillDetailMsg"])

    def test_CarBLeaveHistory(self, userLogin, send_data, expect):
        """查看进出场记录B"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNumB"])
        result = re[0]
        Assertions().assert_in_text(result['enterVipTypeStr'], expect["carBEnterVipTypeStrMsg"])
        Assertions().assert_in_text(result['leaveVipTypeStr'], expect["carBLeaveVipTypeStrMsg"])