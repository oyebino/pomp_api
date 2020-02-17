"""
 Created by lgc on 2020/2/5 15:05.
 微信公众号：泉头活水
"""

import pytest,os
import allure
from time import sleep
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.checkInOut_service import CheckInOut

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data,case_desc = YmlUtils("/test_data/sentry_service/carInOut_controller/messageInOut.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("PC岗亭端业务")
class TestSentryMessage():

    """岗亭收费处理：进场消息、离场消息 """

    def test_sentryMessageIn(self,sentryLogin,send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum1"], 0, send_data["StrictRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["Message1"])

        # 点击进场消息，然后登记放行
        result2 = CheckInOut(sentryLogin).check_car_in_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result2,expect["Message2"])

    def test_sentryMessageOut(self, sentryLogin, send_data, expect):

        # 进场
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 0, send_data["StrictRule_inClientID"])
        result1 = re.json()
        Assertions().assert_in_text(result1, expect["Message1"])

        # 点击进场消息，然后登记放行
        result2 = CheckInOut(sentryLogin).check_car_in_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result2, expect["Message2"])

       # 检查进场记录


        # 离场
        sleep(2)
        re = cloudparking_service().mock_car_in_out(send_data["carNum2"], 1, send_data["StrictRule_outClientID"])
        result3 = re.json()
        Assertions().assert_in_text(result3, expect["Message3"])

        # 点击离场消息，然后登记放行
        result4 = CheckInOut(sentryLogin).check_car_in_out(send_data['lightRule_parkUUID'])
        Assertions().assert_in_text(result4,expect["Message4"])

        # 检查离场记录
