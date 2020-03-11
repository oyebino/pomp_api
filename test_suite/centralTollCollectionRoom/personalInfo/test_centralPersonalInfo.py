"""
 Created by lgc on 2020/3/11 15:11.
 微信公众号：泉头活水
"""

import allure,pytest

from Api.centralTollCollection_service.centralPersonalInfo import CentralPersonalInfo
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/personalInfo.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央值守个人信息")
class TestCentralPersonalInfo(BaseCase):

    def test_centralPersonalInfo(self, centralTollLogin, send_data, expect):
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        # print(re.text)
