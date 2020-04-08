"""
 Created by lgc on 2020/2/11 16:34.
 微信公众号：泉头活水
"""
import allure,pytest
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.sentry_service.personalInfo import PersonalInfo
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/personalInfo.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('岗亭收费处查看个人信息')
class TestPersonalInfo(BaseCase):

    """pc端收费放行"""
    def test_personalInfoBefore(self, sentryLogin, send_data, expect):
        re = PersonalInfo(sentryLogin).dutyInfo()
        result = re.json()
        self.save_data('dealCount', result['deal_count'])
        self.save_data('collectMoney', result['collect_money'])
        Assertions().assert_in_text(result, expect['personalInfoBeforeMsg'])

    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sentryPay(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'],send_data['carHandleType'],'${mytest.carOut_jobId}')
        result = re
        Assertions().assert_in_text(result, expect["sentryPayMsg"])

    def test_personalInfoAfter(self, sentryLogin, send_data, expect):
        re = PersonalInfo(sentryLogin).dutyInfo()
        result = re.json()
        Assertions().assert_in_text(result['deal_count'], expect['dealCount'])
        Assertions().assert_in_text(result['collect_money'], expect['collectMoney'])
