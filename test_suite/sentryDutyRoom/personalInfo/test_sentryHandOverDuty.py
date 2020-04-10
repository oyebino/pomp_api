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

    def test_handOverDuty(self, sentryLogin, send_data, expect):
        """交接班"""
        re = PersonalInfo(sentryLogin).webHandOverDuty(send_data['handUser'], send_data['pwd'])
        self.save_data('handUser', send_data['handUser'])
        self.save_data('pwd', send_data['pwd'])
        result = re
        Assertions().assert_text(result, '')

    @pytest.mark.parametrize('sentryLogin', [{'user': '${mytest.handUser}', 'pwd': '${mytest.pwd}'}],indirect=True)
    def test_offDuty(self, sentryLogin, send_data, expect):
        """下班"""
        re = PersonalInfo(sentryLogin).offduty()
        result = re
        Assertions().assert_text(result, '')
