"""
 Created by lgc on 2020/3/12 9:28.
 微信公众号：泉头活水
"""

import allure,pytest
from Api.sentry_service.personalInfo import PersonalInfo as SentryPersonalInfo
from Api.centralTollCollection_service.centralPersonalInfo import CentralPersonalInfo
from Api.parkingManage_service.tollCollection import TollCollection
from common.BaseCase import BaseCase
from common.utils import YmlUtils
from common.Assert import Assertions

args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/parkingManage/tollCollection/addTollManagerProcess.yml").getData

@pytest.mark.parametrize(args_item, test_data)
@allure.feature("岗亭收费处")
@allure.story('pomp新增-冻结-修改-删除管理员流程')
class TestAddTollManagerProcess(BaseCase):
    """pomp新增-冻结-修改-删除管理员流程"""
    def test_addToll(self,userLogin, send_data, expect):
        """增加管理员"""
        re = TollCollection(userLogin).add_tollCollection(send_data['userId'], send_data['pwd'], send_data['role'])
        self.save_data('userId', send_data['userId'])
        self.save_data('pwd', send_data['pwd'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_bindUserPark(self,userLogin, send_data, expect):
        """绑定用户停车场"""
        re = TollCollection(userLogin).bindUserPark(send_data['parkName'], send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_forceOfDuty(self,userLogin, send_data, expect):
        """强制下班"""
        re = TollCollection(userLogin).forceOfDutyAll()
        result = re
        Assertions().assert_text(result, '全部用户强制下班')

    @pytest.mark.parametrize('sentryLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_loginSentry(self, sentryLogin, send_data, expect):
        """管理员登陆岗亭端收费页面"""
        re = SentryPersonalInfo(sentryLogin).dutyInfo()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])

    @pytest.mark.parametrize('centralTollLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_loginCentral(self, centralTollLogin, send_data, expect):
        """管理员登陆中央收费页面"""
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])

    def test_freezeToll(self, userLogin, send_data, expect):
        """冻结管理员"""
        re = TollCollection(userLogin).freeze_tollCollection(send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_forceOfDutyA(self,userLogin, send_data, expect):
        """强制下班"""
        re = TollCollection(userLogin).forceOfDutyAll()
        result = re
        Assertions().assert_text(result, '全部用户强制下班')

    @pytest.mark.parametrize('sentryLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_freezeTollLoginSentry(self, sentryLogin, send_data, expect):
        """冻结管理员登陆岗亭收费页面"""
        re = SentryPersonalInfo(sentryLogin).dutyInfo()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['freezeLoginMsg'])

    @pytest.mark.parametrize('centralTollLogin', [{'user': '${mytest.userId}', 'pwd': '${mytest.pwd}'}], indirect=True)
    def test_freezeTollLoginCentral(self, centralTollLogin, send_data, expect):
        """冻结管理员登陆中央收费页面"""
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['freezeLoginMsg'])

    def test_unfreezeToll(self, userLogin, send_data, expect):
        """开启管理员"""
        re = TollCollection(userLogin).unfreeze_tollCollection(send_data['userId'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_modifyToll(self, userLogin, send_data, expect):
        """修改管理员"""
        re = TollCollection(userLogin).modify_tollCollection(send_data['userId'],send_data['editUserId'],send_data['editPwd'])
        self.save_data('editUserId',send_data['editUserId'])
        self.save_data('editPwd', send_data['editPwd'])
        result = re['status']
        Assertions().assert_text(result, expect['status'])

    def test_forceOfDutyB(self,userLogin, send_data, expect):
        """强制下班"""
        re = TollCollection(userLogin).forceOfDutyAll()
        result = re
        Assertions().assert_text(result, '全部用户强制下班')

    @pytest.mark.parametrize('sentryLogin', [{'user': '${mytest.editUserId}', 'pwd': '${mytest.editPwd}'}], indirect=True)
    def test_modifyUserLoginSentry(self, sentryLogin, send_data, expect):
        """修改后管理员登陆岗亭端页面"""
        re = SentryPersonalInfo(sentryLogin).dutyInfo()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])

    @pytest.mark.parametrize('centralTollLogin', [{'user': '${mytest.editUserId}', 'pwd': '${mytest.editPwd}'}], indirect=True)
    def test_modifyUserLoginCentral(self, centralTollLogin, send_data, expect):
        """修改后管理员登陆中央收费页面"""
        re = CentralPersonalInfo(centralTollLogin).duty_info()
        onDutyTime = re
        Assertions().assert_in_text(onDutyTime, expect['onDutyTime'])

    def test_delToll(self, userLogin, send_data, expect):
        """删除管理员"""
        re = TollCollection(userLogin).del_tollCollection(send_data['editUserId'])
        status = re['status']
        Assertions().assert_text(status, expect['status'])

    def test_checkDelToll(self, userLogin, send_data, expect):
        """查看已删除管理员是否已删除"""
        re = TollCollection(userLogin).getAllTollCollection()
        result = re
        Assertions().assert_not_in_text(result, expect['isDelToll'])