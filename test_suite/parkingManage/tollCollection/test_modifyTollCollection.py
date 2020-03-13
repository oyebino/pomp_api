"""
 Created by lgc on 2020/3/12 10:28.
 微信公众号：泉头活水
"""

import allure,pytest

from Api.centralTollCollection_service.centralPersonalInfo import CentralPersonalInfo
from Api.parkingManage_service.tollCollection import TollCollection
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/parkingManage/tollCollection/modifyToll.yml").getData


@pytest.mark.parametrize(args_item, test_data)
@allure.feature("收费员账号")
class TestModifyTollection(BaseCase):

    """增加收费员"""

    def test_addToll(self, userLogin, send_data, expect):
        re = TollCollection(userLogin).add_tollCollection(send_data['userId'], send_data['pwd'])
        self.save_data('userId', send_data['userId'])
        self.save_data('pwd', send_data['pwd'])
        status = re.json()
        Assertions().assert_in_text(status, expect['status'])

    """修改收费员"""
    def test_modifyToll(self,userLogin, send_data, expect):
        re = TollCollection(userLogin).modify_tollCollection(send_data['editUserId'], send_data['editPwd'])
        self.save_data('userId', send_data['userId'])
        self.save_data('pwd', send_data['pwd'])
        self.save_data('editUserId', send_data['editUserId'])
        self.save_data('editPwd', send_data['editPwd'])
        status = re.json()
        Assertions().assert_in_text(status, expect['status'])

    """使用之前的用户-登陆中央收费"""
    @pytest.mark.parametrize('centralTollLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_loginCentral(self, centralTollLogin, send_data, expect):
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        onDutyTime = re.json()
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])

    """使用修改后的用户-登陆中央收费"""
    @pytest.mark.parametrize('centralTollLogin', [{'user': '${mytest.editUserId}', 'pwd': '${mytest.editPwd}'}], indirect=True)
    def test_modifyLoginCentral(self, centralTollLogin, send_data, expect):
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        onDutyTime = re.json()
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])