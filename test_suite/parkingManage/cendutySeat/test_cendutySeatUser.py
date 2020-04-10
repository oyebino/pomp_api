#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 11:02
# @Author  : 叶永彬
# @File    : test_cendutySeatUser.py

import allure,pytest
from common.utils import YmlUtils
from Api.parkingManage_service.cendutySeat import CendutySeat
from Api.centerMonitor_service.personalInfo import PersonalInfo
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/parkingManage/cendutySeat/cendutySeatUser.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story("新增-修改-删除远程值班帐户")

class TestCendutySeatUser(BaseCase):
    """远程值班帐户管理"""
    def test_addCendutySeat(self, userLogin, send_data, expect):
        """新增远程值班帐户"""
        re = CendutySeat(userLogin).addCendutySeat(send_data['userId'], send_data['userName'], send_data['pwd'])
        self.save_data('userId',send_data['userId'])
        self.save_data('pwd',send_data['pwd'])
        result = re['status']
        Assertions().assert_text(result, expect['addCendutySeatMsg'])

    @pytest.mark.parametrize('centerMonitorLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_loginCendutySeat(self,centerMonitorLogin, send_data, expect):
        """新增远程值班账号登录"""
        re = PersonalInfo(centerMonitorLogin).getCendutySeat()
        result = re['userid']
        Assertions().assert_text(result, expect['loginCendutySeatMsg'])

    def test_lockCendutySeat(self, userLogin, send_data, expect):
        """冻结远程值班帐户"""
        re = CendutySeat(userLogin).lockCendutySeat(send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['lockCendutySeatMsg'])

    # @pytest.mark.parametrize('centerMonitorLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    # def test_lockLoginCendutySeat(self,centerMonitorLogin, send_data, expect):
    #     """冻结远程值班账号登录"""
    #     re = PersonalInfo(centerMonitorLogin).getCendutySeat()
    #     result = re['message']
    #     Assertions().assert_text(result, expect['lockLoginCendutySeatMsg'])

    def test_startCendutySeat(self, userLogin, send_data, expect):
        """开启远程值班帐户"""
        re = CendutySeat(userLogin).startCendutySeat(send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['startCendutySeatMsg'])

    # @pytest.mark.parametrize('centerMonitorLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    # def test_startLoginCendutySeat(self,centerMonitorLogin, send_data, expect):
    #     """新增远程值班账号登录"""
    #     re = PersonalInfo(centerMonitorLogin).getCendutySeat()
    #     result = re['userid']
    #     Assertions().assert_text(result, expect['loginCendutySeatMsg'])

    def test_updateCendutySeat(self, userLogin, send_data, expect):
        """修改远程值班帐户"""
        re = CendutySeat(userLogin).updateCendutySeat(send_data['userId'], send_data['editUserName'])
        result = re['status']
        Assertions().assert_text(result, expect['updateCendutySeatMsg'])

    def test_checkEditCendutySeatList(self, userLogin, send_data, expect):
        """查看远程值班帐户"""
        re = CendutySeat(userLogin).cendutySeatList(send_data['editUserName'])
        result = re
        Assertions().assert_in_text(result, expect['checkEditCendutySeatListMsg'])

    def test_deleteCendutySeat(self, userLogin, send_data, expect):
        """删除远程值班帐户"""
        re = CendutySeat(userLogin).deleteCendutySeat(send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['deleteCendutySeatMsg'])

    def test_checkDeleteCendutySeatList(self, userLogin, send_data, expect):
        """查看远程值班帐户"""
        re = CendutySeat(userLogin).cendutySeatList(send_data['editUserName'])
        result = re
        Assertions().assert_not_in_text(result, expect['checkDeleteCendutySeatMsg'])