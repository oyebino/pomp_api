"""
 Created by lgc on 2020/2/26 17:25.
 微信公众号：泉头活水
"""
import allure
import pytest

from Api.centerMonitor_service.personalInfo import CenterPersonalInfo
from Api.cloudparking_service import cloudparking_service
from Api.sentry_service.carInOutHandle import CarInOutHandle
from common.Assert import Assertions
from common.BaseCase import BaseCase
from common.utils import YmlUtils

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/centerMonitorRoom/personalInfo/operatorLog.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("中央值守操作日志")
class TestOperatorLog(BaseCase):

    # def test_mockCarIn(self, send_data, expect):
    #     """模拟进场"""
    #     re = cloudparking_service().mockCarInOut(send_data["carNum"], 0, send_data["StrictRule_inClientID"])
    #     result = re.json()
    #     self.save_data('carIn_jobId', result['biz_content']['job_id'])
    #     Assertions().assert_in_text(result, expect["mockCarInMessage"])
    #
    # def test_checkIn(self, sentryLogin, send_data, expect):
    #     """登记放行-此处应为中央值守的登记放行-未完成"""
    #     re = CarInOutHandle(sentryLogin).carInOutHandle(send_data['carNum'], send_data['carInHandleType'],send_data['carIn_jobId'])
    #     result = re.json()['biz_content']['result']
    #     Assertions().assert_in_text(result['screen'], expect["checkCarInScreen"])
    #     Assertions().assert_in_text(result['voice'], expect["checkCarInVoice"])
    #     Assertions().assert_in_text(result['open_gate'], expect["checkCarInOpenGate"])


    def test_operatorLog(self,centerMonitorLogin, send_data, expect):
        """检查操作日志-是否有登记放行-未完成"""
        re = CenterPersonalInfo(centerMonitorLogin).logList()
        print(re.text)
        # Assertions().assert_in_text(re, expect['collectMoney'])
