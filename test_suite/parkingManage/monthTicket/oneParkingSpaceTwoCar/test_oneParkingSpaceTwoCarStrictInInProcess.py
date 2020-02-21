#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/02/07 14:35
# @Author  : 何涌
# @File    : test_oneParkingSpaceTwoCarStrictInInProcess.py

import pytest,os
import allure
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from Api.information_service.information import Information
from common.Assert import Assertions
from Api.cloudparking_service import cloudparking_service

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/monthTicket/oneParkingSpaceTwoCar/oneParkingSpaceTwoCarStrictInInProcess.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("月票管理模块")
class TestOneParkingSpaceTwoCarStrictInInProcess():
    """多位多车VIP转临时车严进"""

    # 多位多车VIP第一辆车进车
    def test_mockCarIn1(self, send_data, expect):
        """模拟车辆进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_presentCar1(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, send_data["carNum"])
        Assertions().assert_in_text(result, send_data["ticketName"])

    # 多位多车VIP第二辆车进车
    def test_mockCarIn2(self,send_data,expect):
        re = cloudparking_service().mock_car_in_out(send_data['carNum2'],0,send_data['strictInClientID'])
        result = re.json()
        self.save_data('carIn_jobId',result['biz_content']['job_id'])
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCheckCarIn2(self,send_data,expect):
        re = cloudparking_service().check_car_in(send_data['carNum2'],send_data['carInJobId'])
        result = re.json()['biz_content']['result']['open_gate']
        Assertions().assert_in_text(result, expect["isOpenGate"])

    def test_presentCar2(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["presentCarMessage"])
        Assertions().assert_in_text(result, expect["carNum2"])
        Assertions().assert_in_text(result, expect["carType"])

    # 多位多车VIP第一辆车出车
    def test_mockCarOut1(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"],1,send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mock_car_in"])
        Assertions().assert_in_text(result, expect["inscreen"])
        Assertions().assert_in_text(result, expect["invoice"])

    def test_CarLeaveHistory1(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, expect["carNum"])

    # 第二辆车中央缴费
    def test_centralPay(self,send_data,expect):
        """中央缴费"""
        re = Information().centralPay(send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["centralPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkId"],send_data["carNum2"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result,expect["parkingBillDetailMessage"])

    # 多位多车VIP第二辆车出车
    def test_mockCarOut2(self, send_data, expect):
        """模拟车辆离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"],1,send_data["outClientID"])
        result = re.json()
        screen = "{}\\\\{}".format(send_data["carNum2"], send_data["mockCarOutMessage"])
        voice = "${}${}".format(send_data["carNum2"], send_data["mockCarOutMessage"])
        Assertions().assert_in_text(result, expect["mock_car_out"])
        Assertions().assert_in_text(result, screen)
        Assertions().assert_in_text(result, voice)

    def test_CarLeaveHistory2(self, userLogin, send_data, expect):
        """查看进出场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkId"], send_data["carNum2"])
        result = re.json()
        Assertions().assert_in_text(result, expect["CarLeaveHistoryMessage"])
        Assertions().assert_in_text(result, send_data["carNum2"])