"""
 Created by lgc on 2020/2/19 15:37.
 微信公众号：泉头活水
"""

import os

import allure
import pytest

from Api.aomp_service.getActivation import ActivationInfo
from Api.parkingManage_service.createParking import CreateParking, Operation_parking

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, "../.."))
from common.utils import YmlUtils


args_item = "send_data,expect"
test_data, case_desc = YmlUtils("/test_data/parkingManage/parkConfig/createParking.yml").getData
@pytest.mark.parametrize(args_item, test_data)
@allure.feature("创建停车场")

class Test_createParking():

    """添加授权商"""
    def test_add_cooperative_use(self,aompLogin, send_data, expect):
        ActivationInfo(aompLogin).add_cooperative_user(send_data['cooperativeAccount'])

    """获取激活码"""
    def test_get_activation(self, aompLogin, send_data, expect):
        ActivationInfo(aompLogin).get_activation(send_data['cooperativeAccount'])

    """注册运营商"""
    def test_createPomp(self, send_data, expect):

        Operation_parking().validateActivationCode(send_data['cooperativeAccount'])
        Operation_parking().validAndregister_User(send_data['cooperativeAccount'], send_data['userAccount'])

    """新增停车场"""
    def test_createParking(self, userLogin, send_data, expect):
        CreateParking(userLogin).newParking(send_data['cooperativeAccount'])
        # CreateParking(userLogin).newParking("test20200219165316")

