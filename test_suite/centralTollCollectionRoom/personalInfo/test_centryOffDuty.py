#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/27 15:50
# @Author  : 叶永彬
# @File    : test_centryOffDuty.py

import allure,pytest
from common.utils import YmlUtils
from Api.centralTollCollection_service.centralPersonalInfo import CentralPersonalInfo
from common.Assert import Assertions
from common.BaseCase import BaseCase

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/centralTollCollectionRoom/personalInfo/centryOffDuty.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央收费处")
@allure.story('中央收费处-下班')
class TestCentryOffDuty(BaseCase):

    def test_centralOffDuty(self, centralTollLogin, send_data,expect):
        """收费处下班"""
        re = CentralPersonalInfo(centralTollLogin).centralOffDuty()
        result = re
        Assertions().assert_text(result, "")
        Assertions().assert_text(re.status_code, expect['status_code'])