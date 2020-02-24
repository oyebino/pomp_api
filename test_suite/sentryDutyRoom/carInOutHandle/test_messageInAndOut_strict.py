"""
 Created by lgc on 2020/2/5 15:05.
 微信公众号：泉头活水
"""

import pytest,os
import allure
from time import sleep
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/messageInOut.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("PC岗亭进出场消息处理")
class TestSentryMessage():

    """岗亭收费处理：进场、离场消息 """

    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["StrictRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkMessageIn(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).check_car_in_out(send_data['carNum'])
        result = re.json()["success"]
        Assertions().assert_in_text(result, expect["checkInMessage"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["StrictRule_outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkMessageOut(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).check_car_in_out(send_data['carNum'])
        result = re.json()["success"]
        Assertions().assert_in_text(result, expect["checkOutMessage"])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])

