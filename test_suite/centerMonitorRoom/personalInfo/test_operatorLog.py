"""
 Created by lgc on 2020/2/26 17:25.
 微信公众号：泉头活水
"""
import allure,pytest
from common.utils import YmlUtils
from Api.cloudparking_service import cloudparking_service
from Api.centerMonitor_service.carInOutHandle import CarInOutHandle
from Api.centerMonitor_service.personalInfo import PersonalInfo
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/centerMonitorRoom/personalInfo/operatorLog.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("远程值班室")
@allure.story('远程值班室查看操作日志')
class TestOperatorLog():

    def test_mockCarIn(self,send_data,expect):
        """模拟车辆进场"""
        re = cloudparking_service().mockCarInOut(send_data["carNum"],0,send_data["inClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarInMessage"])

    def test_mockCarOut(self, centerMonitorLogin, send_data,expect):
        """模拟离场"""
        re = cloudparking_service(centerMonitorLogin).mockCarInOut(send_data["carNum"], 1, send_data["outClientID"])
        result = re.json()
        Assertions().assert_in_text(result, expect["mockCarOutMessage"])

    def test_sendVoiceMsg(self, centerMonitorLogin, send_data,expect):
        """发送语音"""
        re = CarInOutHandle(centerMonitorLogin).sendVoiceMessage(send_data["carNum"], send_data['voiceMsg'])
        result = re['status']
        Assertions().assert_text(result, expect["sendVoiceMsg"])

    def test_operatorLog(self,centerMonitorLogin, send_data, expect):
        """检查操作日志-是否有登记放行-未完成"""
        re = PersonalInfo(centerMonitorLogin).logList()
        result = re[0]
        Assertions().assert_in_text(result['handleMessage'], expect['operatorLogMsg'])
