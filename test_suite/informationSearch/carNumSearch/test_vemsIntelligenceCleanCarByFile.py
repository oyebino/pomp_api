#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/13 17:13
# @Author  : 叶永彬
# @File    : test_vemsIntelligenceCleanCarByFile.py

import allure,pytest
from common.utils import YmlUtils
from Api.information_service.information import Information
from Api.offLineParking_service.openYDTReq import OpenYDTReq
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/informationSearch/carNumSearch/vemsIntelligenceCleanCarByFile.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("信息查询-车辆查询")
@allure.story('vems智能盘点-按表格上传方式盘离')
class TestVemsIntelligenceCleanCarByFile(BaseCase):
    """智能盘点，选择vems，然后按在场车辆盘点，上传盘点表格，上传成功后，勾选“将未匹配的车辆补录进场”，点击确定后，不在表格中的车辆都被盘点走，
    在在场车辆中查看不到被盘点走的车辆，在异常进场中可以查看到该被盘点走的车辆，并且未匹配的车辆以当前时间补录到在场车辆中"""

    def test_mockCarInA(self,openYDTLogin,send_data,expect):
        """模拟车辆A进场"""
        re = OpenYDTReq(openYDTLogin).carInOut(send_data["parkCode"],send_data["carNumA"],0)
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarInB(self,openYDTLogin,send_data,expect):
        """模拟车辆B进场"""
        re = OpenYDTReq(openYDTLogin).carInOut(send_data["parkCode"],send_data["carNumB"],0)
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_intelligenceUploadFile(self, userLogin, send_data, expect):
        """上传盘点表格并-勾选-将未匹配的车辆C补录进场"""
        re = Information(userLogin).intelligenceCheckCarOut(send_data['parkName'],send_data['cleanType'], send_data['carNumList'])
        result = re['status']
        Assertions().assert_text(result, expect["cleanCarCheckOutMsg"])

    def test_checkPresentCar(self, userLogin, send_data, expect):
        """在场车辆中查看不到A车辆,能查到B车辆"""
        re = Information(userLogin).getPresentCar(send_data['parkName'])
        result = re
        Assertions().assert_not_in_text(result, expect["checkPresentCarA"])
        Assertions().assert_in_text(result, expect["checkPresentCarB"])

    def test_checkPresentCarC(self, userLogin, send_data, expect):
        """在场车辆中查看C车辆,前入场时间为盘点时间"""
        re = Information(userLogin).getPresentCar(send_data['parkName'], send_data['carNumC'])
        result = re[0]
        Assertions().assert_text(result['checkInTypeStr'], expect['checkPresentCarC'])

    def test_checkAbnormalInCar(self, userLogin, send_data, expect):
        """异常进场中可以查看到A车辆"""
        re = Information(userLogin).getAbnormalInCar(send_data['parkName'], send_data['carNumA'])
        result = re
        Assertions().assert_in_text(result, expect["checkAbnormalInCar"])