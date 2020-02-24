"""
 Created by lgc on 2020/2/9 19:10.
 微信公众号：泉头活水
"""

import allure,os
import pytest

from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/recordInOut.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("pc查看进出场记录")


class TestSentryRecordInOut():

    """pc查看进出场记录"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_recordIn(self, sentryLogin, send_data, expect):
        """在pc端查看进场记录"""
        re = CarInOutHandle(sentryLogin).record_car_in(send_data['carNum'])
        result = re.json()['rows'][0]['carCode']
        Assertions().assert_in_text(result, expect['carNum'])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mock_car_in_out(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect['mockCarOutMessage'])

    def test_checkOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).normal_car_out(send_data['carNum'])
        result = re.json()["success"]
        Assertions().assert_in_text(result, expect["checkOutMessage"])

    def test_recordOut(self, sentryLogin, send_data, expect):

        """在pc端查看离场记录"""
        re = CarInOutHandle(sentryLogin).record_car_out(send_data['carNum'])
        result = re.json()['rows'][0]['carCode']
        Assertions().assert_in_text(result, expect['carNum'])