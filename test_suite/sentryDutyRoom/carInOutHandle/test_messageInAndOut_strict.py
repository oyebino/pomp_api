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
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/carInOutHandle/messageInOut.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('PC岗亭进出场消息处理')
class TestSentryMessage(BaseCase):

    """岗亭收费处理：进场、离场消息 """

    def test_mockCarIn(self,sentryLogin, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["StrictRule_inClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_checkMessageIn(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carInHandleType'],send_data['carIn_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])
        Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
        Assertions().assert_in_text(result['open_gate'], expect["checkCarInOpenGate"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["StrictRule_outClientID"])
        result = re
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_checkMessageOut(self, sentryLogin, send_data, expect):
        """登记放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carOutHandleType'], send_data['carOut_jobId'])
        result = re
        Assertions().assert_in_text(result['screen'], expect['checkCarOutScreen'])
        Assertions().assert_in_text(result['voice'], expect['checkCarOutVoice'])
        Assertions().assert_in_text(result['open_gate'], expect['checkCarOutOpenGate'])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["parkName"], send_data["carNum"])
        result = re
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])

