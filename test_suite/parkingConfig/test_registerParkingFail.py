#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/3 14:28
# @Author  : 叶永彬
# @File    : test_registerParkingFail.py

import allure,pytest
from common.utils import YmlUtils
from Api.aomp_service.cooperativeManage import CooperativeManage
from Api.index_service.registerParking import RegisterParking
from Api.index_service.index import Index
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingConfig/registerParkingFail.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("注册停车场")
@allure.story('注册-上线相同名称的停车场失败场景')
class TestRegisterParkingFail(BaseCase):
    """新增车场"""
    def test_getActivationCode(self, aompLogin, send_data, expect):
        """在aomp获取激活码"""
        result = CooperativeManage(aompLogin).getCooperativeCode(send_data['cooperativeName'])
        self.save_data('activationCode', result)
        Assertions().assert_in_text(result,expect['getActivationCodeMsg'])

    def test_registerUser(self, userLogin, send_data, expect):
        """注册用户"""
        re = RegisterParking(userLogin).registerUser(send_data['activationCode'],send_data['managerName'],send_data['userAccount'],send_data['pwd'])
        self.save_data('userAccount',send_data['userAccount'])
        self.save_data('pwd',send_data['pwd'])
        result = re
        Assertions().assert_text(result['message'], expect['registerUserMsg'])

    @pytest.mark.parametrize('userLogin', [{'user': '${mytest.userAccount}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_addOperatorPark(self,userLogin, send_data, expect):
        """创建用户车场"""
        re = RegisterParking(userLogin).addOperatorPark(send_data['activationCode'],send_data['parkName'])
        result = re
        Assertions().assert_text(result['message'], expect['addOperatorParkMsg'])
