"""
 Created by lgc on 2020/2/9 19:10.
 微信公众号：泉头活水
"""

import allure,os
import pytest

from time import sleep
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.checkInOut_service import CheckInOut
from Api.sentry_service.recordInOut_service import RecordInOut

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentry_service/carInOut_controller/recordInOut.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("PC岗亭端业务")


class TestSentryRecordInOut():

    def test_sentryRecordIn(self,sentryLogin, send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum1"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect['Message1'])

        # 查看进场记录
        result2 = RecordInOut(sentryLogin).record_car_in()
        Assertions().assert_in_text(result2, expect['carNum1'])


    def test_sentryCheckOut(self, sentryLogin, send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 0, send_data["lightRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect['Message1'])

        # 离场
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 1, send_data["lightRule_outClientID"])
        result2 = re.json()
        Assertions().assert_in_text(result2, expect['Message2'])

        # 点击收费放行
        result3 = CheckInOut(sentryLogin).normal_car_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result3, expect["Message3"])
        sleep(2)

        # 查看离场记录
        result4 = RecordInOut(sentryLogin).record_car_out()
        Assertions().assert_in_text(result4, expect['carNum2'])
