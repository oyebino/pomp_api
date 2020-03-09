"""
 Created by lgc on 2020/2/11 16:34.
 微信公众号：泉头活水
"""
import allure,pytest
from Api.cloudparking_service import cloudparking_service
from Api.information_service.information import Information
from Api.sentry_service.carInOutHandle import CarInOutHandle
from Api.sentry_service.personalInfo import PersonalInfo
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/sentryDutyRoom/personalInfo/personalInfo.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("pc端收费放行")
class TestPersonalInfo(BaseCase):

    """pc端收费放行"""
    def test_mockCarIn(self, send_data, expect):
        """模拟进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["lightRule_inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_presentCar(self, userLogin, send_data, expect):
        """查看在场记录"""
        re = Information(userLogin).getPresentCar(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["presentCarMessage"])

    def test_mockCarOut(self, send_data, expect):
        """模拟离场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"], 1, send_data["lightRule_outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_personalInfoBefore(self, sentryLogin, send_data, expect):
        re = PersonalInfo(sentryLogin).dutyInfo()
        self.save_data('dealCount', re.json()['deal_count'])
        self.save_data('collectMoney', re.json()['collect_money'])
        Assertions().assert_in_text("on_duty_time", expect['onDutyTime'])

    def test_CheckOut(self, sentryLogin, send_data, expect):
        """收费放行"""
        re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'])
        result = re.json()["success"]
        Assertions().assert_in_text(result, expect["checkOutMessage"])

    def test_personalInfoAfter(self, sentryLogin, send_data, expect):
        re = PersonalInfo(sentryLogin).dutyInfo()
        new_deal_count = int(re.json()['deal_count']) - 1
        collect_money = float(re.json()['collect_money']) - 5  # 收费规则需固定
        Assertions().assert_in_text(new_deal_count, expect['dealCount'])
        Assertions().assert_in_text(collect_money, expect['collectMoney'])

    def test_carLeaveHistory(self, userLogin, send_data, expect):
        """查看离场记录"""
        re = Information(userLogin).getCarLeaveHistory(send_data["lightRule_parkID"], send_data["carNum"])
        result = re.json()["data"]["rows"]
        Assertions().assert_in_text(result, expect["carLeaveHistoryMessage"])
