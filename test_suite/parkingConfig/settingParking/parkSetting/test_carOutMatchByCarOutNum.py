#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/18 17:09
# @Author  : 叶永彬
# @File    : test_carOutMatchByCarOutNum.py

import allure,pytest
from common.utils import YmlUtils
from common.BaseCase import BaseCase
from Api.information_service.information import Information
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.parkingConfig_service.parkingSetting import ParkingSetting
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/settingParking/parkSetting/carOutMatchByCarOutNum.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("智泊云-配置停车场-车场配置")
@allure.story('临时车离场模糊匹配-最终车牌为出场车牌')
class TestCarOutMatchByCarOutNum(BaseCase):
    """临时车离场模糊匹配（最终车牌为出场车牌）"""
    def test_enableMatchCarNum(self,userLogin,send_data,expect):
        """开启模糊匹配功能"""
        re = ParkingSetting(userLogin).updataOperatorParkCofigInfo(send_data['parkName'], send_data['settingName'], 1)
        result = re['status']
        Assertions().assert_text(result, 1)

    def test_mockCarIn(self,send_data,expect):
        re = cloudparking_service().mockCarInOut(send_data['carNumIn'],0,send_data['inClientID'],send_data['carNumInConfidence'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_presentCar(self,userLogin,send_data,expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["parkName"],send_data["carNumIn"])
        result = re
        Assertions().assert_in_text(result,expect["presentCarMessage"])

    def test_mockCarOut(self,send_data,expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data['carNumOut'],1,send_data['outClientID'],send_data['carNumOutConfidence'])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self,sentryLogin,send_data,expect):
        """岗亭端缴费"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data["carNumOut"],send_data['carHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMessage"])

    def test_parkingBillDetail(self,userLogin,send_data,expect):
        """查看收费记录"""
        re = Information(userLogin).getParkingBillDetail(send_data["parkName"],send_data["carNumOut"])
        result = re
        Assertions().assert_in_text(result,expect["parkingBillDetailMessage"])

    def test_carLeaveHistory(self,userLogin,send_data,expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"],send_data["carNumOut"])
        result = re
        Assertions().assert_in_text(result,expect["carLeaveHistoryMessage"])

    def test_disableMatchCarNum(self,userLogin,send_data,expect):
        """关闭模糊匹配功能"""
        re = ParkingSetting(userLogin).updataOperatorParkCofigInfo(send_data['parkName'], send_data['settingName'], 0)
        result = re['status']
        Assertions().assert_text(result, 1)

    def test_isMatchCarNumConfig(self, userLogin,send_data,expect):
        """查看模糊匹配功能是否关闭"""
        re = ParkingSetting(userLogin).getOperatorParkConfigInfo(send_data['parkName'])
        result = re['parkCloudDetailVo']
        Assertions().assert_body(result, 'openFuzzyMatch', 'false')
