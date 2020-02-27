"""
 Created by lgc on 2020/2/5 15:05.
 微信公众号：泉头活水
"""

import pytest,os
import allure

from Api.Login import SentryLogin
from Api.sentry_service.personalInfo import SentryLogin as SLogin
from Api.sentry_service.personalInfo import PersonalInfo

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/login.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("登录或退出PC岗亭")
class TestSentryLogin():

    """登录pc岗亭,注意本案例登录部分通道"""
    def test_Login(self,send_data,expect):
        s = SLogin()
        s.login(send_data["user_id"],send_data["password"])
        s.select_channel(send_data['lightRule_inChannelCode'],send_data['lightRule_outChannelCode'])
        status = s.status()
        Assertions().assert_in_text(status,expect["loginMessage1"])

    """退出pc岗亭,注意本案例登录部分通道"""
    def test_Quit(self,send_data,expect):
        s = SLogin()
        s.login(send_data["user_id"], send_data["password"])
        s.select_channel(send_data['lightRule_inChannelCode'],send_data['lightRule_outChannelCode'])
        status1 = s.status()
        Assertions().assert_in_text(status1, expect["loginMessage1"])
        s.quit()
        status2 = s.status()
        print("***status***",status2)
        Assertions().assert_in_text(status2,expect["loginMessage2"])

    """登录pc岗亭,全部通道"""
    def test_LoginAllChannel(self,sentryLogin, send_data, expect):
        # 登录
        SentryLogin().login()

        # 检查数据库，待定

        # Assertions().assert_in_text(status,expect["loginMessage1"])

    """退出pc岗亭,全部通道"""
    def test_QuitAllChannel(self,sentryLogin, send_data, expect):
        PersonalInfo(sentryLogin).offduty()

        # 检查数据库，待定
        # Assertions().assert_in_text(status2,expect["loginMessage2"])
