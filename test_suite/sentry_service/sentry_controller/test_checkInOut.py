"""
 Created by lgc on 2020/2/11 16:34.
 微信公众号：泉头活水
"""

import pytest,os
import allure

from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.checkInOut_service import CheckInOut

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentry_service/carInOut_controller/checkInOut.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("PC岗亭端业务")
class TestCheckInOut():
    ''''收费放行'''

    def test_CheckOut(self, sentryLogin, send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["Message1"])

        # 离场
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result2 = re.json()
        Assertions().assert_in_text(result2, expect["Message2"])

        # 点击收费放行
        id = CheckInOut(sentryLogin).check_message_in_out()
        result3 = CheckInOut(sentryLogin).normal_car_out(id)
        Assertions().assert_in_text(result3, expect["Message3"])

        # 检查进出场记录-待补充

    def test_CheckAbnormalOut(self, sentryLogin, send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["Message1"])

        # 离场
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result2 = re.json()
        Assertions().assert_in_text(result2, expect["Message2"])

        # 点击收费放行
        id = CheckInOut(sentryLogin).check_message_in_out()
        result3 = CheckInOut(sentryLogin).abnormal_car_out(id)
        Assertions().assert_in_text(result3, expect["Message3"])

        # 检查进出场记录-待补充
