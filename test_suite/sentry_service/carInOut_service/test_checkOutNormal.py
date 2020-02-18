"""
 Created by lgc on 2020/2/11 16:34.
 微信公众号：泉头活水
"""

import pytest,os
import allure

from Api.cloudparking_service import cloudparking_service
from Api.information_service.information_controller import Information_controller
from Api.sentry_service.carInOut_service.checkInOut_service import CheckInOut

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentry_service/carInOut_service/checkInOut.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("pc端收费放行")
class TestCheckOutNormal():

    """pc端收费放行"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["mockCarInMessage"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information_controller(userLogin).getPresentCar(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["presentCarMessage"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result2 = re.json()
        Assertions().assert_in_text(result2, expect["mockCarOutMessage"])

    def test_CheckOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        result3 = CheckInOut(sentryLogin).normal_car_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result3, expect["checkOutMessage"])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information_controller(userLogin).getCarLeaveHistory(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])
