"""
 Created by lgc on 2020/2/26 17:25.
 微信公众号：泉头活水
"""
import allure
import pytest

from Api.centerMonitor_service.personalInfo import CenterPersonalInfo
from common.Assert import Assertions
from common.BaseCase import BaseCase
from common.utils import YmlUtils

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/centerMonitorRoom/personalInfo/personalInfo.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央值守操作日志")
class TestPersonalInfo(BaseCase):

    def test_aa(self,centerMonitorLogin, send_data, expect):
        re = CenterPersonalInfo(centerMonitorLogin).logList()
        # print(re.text)
        # Assertions().assert_in_text(re, expect['collectMoney'])
