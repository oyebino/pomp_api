#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/2 15:26
# @Author  : 叶永彬
# @File    : test_sentryHandOverDuty.py

import allure,pytest
from Api.sentry_service.personalInfo import PersonalInfo
from Api.parkingManage_service.tollCollection import TollCollection
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/sentryHandOverDuty.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处收费员交接班-下班')
class TestSentryHandOverDuty(BaseCase):
    """岗亭收费处收费员交接班"""
    def test_addToll(self,userLogin, send_data, expect):
        """增加收费员"""
        re = TollCollection(userLogin).add_tollCollection(send_data['handUser'], send_data['pwd'], send_data['role'])
        self.save_data('handUser', send_data['handUser'])
        self.save_data('pwd', send_data['pwd'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_bindUserPark(self,userLogin, send_data, expect):
        """绑定用户停车场"""
        re = TollCollection(userLogin).bindUserPark(send_data['parkName'], send_data['handUser'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_handOverDuty(self, sentryLogin, send_data, expect):
        """交接班"""
        re = PersonalInfo(sentryLogin).webHandOverDuty(send_data['handUser'], send_data['pwd'])
        result = re.text
        Assertions().assert_text(result, '')
        Assertions().assert_text(re.status_code, expect['handOverDutyStatusCode'])

    @pytest.mark.parametrize('sentryLogin', [{'user': '${mytest.handUser}', 'pwd': '${mytest.pwd}'}],indirect=True)
    def test_offDuty(self, sentryLogin, send_data, expect):
        """下班"""
        re = PersonalInfo(sentryLogin).offduty()
        result = re.text
        Assertions().assert_code(re.status_code, expect['offdutyStatusCode'])
        Assertions().assert_text(result, '')

    def test_delToll(self, userLogin, send_data, expect):
        """删除收费员"""
        re = TollCollection(userLogin).del_tollCollection(send_data['handUser'])
        status = re['status']
        Assertions().assert_text(status, expect['status'])

