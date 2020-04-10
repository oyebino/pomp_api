"""
 Created by lgc on 2020/2/9 19:10.
 微信公众号：泉头活水
"""

import pytest,allure
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/recordInOut.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处查看进场-出场记录')

class TestSentryRecordInOut(BaseCase):
    """pc查看进出场记录"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_recordIn(self, sentryLogin, send_data, expect):
        """在pc端查看进场记录"""
        re = CarInOutHandle(sentryLogin).getCarInRecord(send_data['carNum'], send_data['parkName'])
        result = re[0]
        Assertions().assert_in_text(result['carCode'], expect['recordInMsg'])

    def test_mockCarout(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result = re
        Assertions().assert_in_text(result, expect['mockCarOutMessage'])

    def test_checkOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carOutHandleType'], send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_recordOut(self, sentryLogin, send_data, expect):

        """在pc端查看离场记录"""
        re = CarInOutHandle(sentryLogin).getCarOutRecord(send_data['carNum'], send_data['parkName'])
        result = re[0]
        Assertions().assert_text(result['carCode'], expect['recordOutCarNum'])
        Assertions().assert_in_text(result['payVal'], expect['recordOutPayVal'])