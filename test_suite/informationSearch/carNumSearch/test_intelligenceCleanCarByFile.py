#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 17:13
# @Author  : 叶永彬
# @File    : test_intelligenceCleanCarByFile.py

import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/carNumSearch/intelligenceCleanCarByFile.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询")
class TestIntelligenceCleanCarByFile(BaseCase):
    """智能盘点，选择智泊云车场，然后按在场车辆盘点，上传盘点表格，上传成功后，勾选“将未匹配的车辆补录进场”，点击确定后，不在表格中的车辆都被盘点走，
    在在场车辆中查看不到被盘点走的车辆，在异常进场中可以查看到该被盘点走的车辆，并且未匹配的车辆以当前时间补录到在场车辆中"""

    def test_mockCarInA(self,send_data,expect):
        """模拟车辆A进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumA"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarInB(self,send_data,expect):
        """模拟车辆B进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNumB"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_intelligenceUploadFile(self, userLogin, send_data, expect):
        """上传盘点表格并-勾选-将未匹配的车辆C补录进场"""
        re = Information(userLogin).intelligenceCheckCarOut(send_data['parkName'],send_data['cleanType'], send_data['carNumList'])
        result = re.json()['status']
        Assertions().assert_text(result, expect["cleanCarCheckOutMsg"])

    def test_checkPresentCar(self, userLogin, send_data, expect):
        """在场车辆中查看不到A车辆,能查到B车辆"""
        re = Information(userLogin).getPresentCar(send_data['parkName'])
        result = re.json()['data']['rows']
        Assertions().assert_not_in_text(result, expect["checkPresentCarA"])
        Assertions().assert_in_text(result, expect["checkPresentCarB"])

    def test_checkPresentCarC(self, userLogin, send_data, expect):
        """在场车辆中查看C车辆,前入场时间为盘点时间"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNumC'])
        result = re.json()['data']['rows'][0]
        Assertions().assert_text(result['checkInTypeStr'], expect['checkPresentCarC'])

    def test_checkAbnormalInCar(self, userLogin, send_data, expect):
        """异常进场中可以查看到A车辆"""
        re = Information(userLogin).getAbnormalInCar(send_data['parkName'], send_data['carNumA'])
        result = re.json()['data']['rows']
        Assertions().assert_in_text(result, expect["checkAbnormalInCar"])