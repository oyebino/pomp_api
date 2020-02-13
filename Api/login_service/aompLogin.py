"""
 Created by lgc on 2019/12/24 16:01.
 微信公众号：泉头活水
"""
import json
import time
import requests

from Api.login_service.create_parking import CreateParking
from Api.login_service.pompLogin import pomp, Operation_parking
from common.db import Db as db
from common.superAction import SuperAction


class aomp(object):
    cooperativeAccount = 'test'+SuperAction().get_time()

    """校验验证码"""
    def __init__(self, host="http://aomp-grey.k8s.yidianting.com.cn"):
        self.host = host
        loginUrl = self.host + "/checkLogin.do"
        self.S = requests.session()
        data = {
            "user": "lgc",
            "pwd": "999999",
            "validateCode": "9999",
            "isOnLine": "isOnLine",
            "flag": "-1"
        }
        self.S.post(loginUrl, data)

    def login(self):
        """登陆aomp"""
        path = self.host + "/admin/loginTomanage.do?flag=admin&flag=admin"
        data = {
            "flag": "admin"
        }
        self.S.post(path, data)

    def add_cooperative_user(self, cooperativeAccount):
        """添加授权商"""
        path = self.host + "/cooperativeUser/saveCooperativeUser.do"
        data = {
            "cooperativeName": "test合作商{}".format(SuperAction().get_time()),
            "cooperativeAccount": "{}".format(cooperativeAccount),
            "cooperativePassword": "999999",
            "isOkPassword": "999999",
            "weixinAccountId": "2"
        }
        self.S.post(path, data)

    def add_activation(self, cooperativeUserId):
        """新增并生成激活码"""

        path_add = self.host + "/cooperativeCode/addCooperativeActivation.do"
        data_add = {
            "cooperativeUserId": "{}".format(cooperativeUserId),
            "codeTotal": "10"
        }
        self.S.post(path_add, data_add)

    def pro_activation(self, cooperativeUserId, activationId):
        path_pro = self.host + "/cooperativeCode/produceCode.do"
        data_pro = {
            "cooperativeUserId": "{}".format(cooperativeUserId),
            "activationId": "{}".format(activationId)
        }
        self.S.post(path_pro, data_pro)

    def getCodeDetail(self, activationId):
        """新增并生成激活码、获取激活码"""
        path = self.host + "/cooperativeCode/getCodeDetail.do"
        data = {
            "page": 1,
            "rows": "10",
            "activationId": "{}".format(activationId)
        }
        r = self.S.post(path, data)
        print(r.text)
        print(type(r.text))
        s = json.loads(r.text)
        return s['rows'][0]['activationCode']

    def main(self):
        """登陆aomp-新增合作商-新增激活码-生成激活码-获取激活码"""
        self.login()
        self.add_cooperative_user(self.cooperativeAccount)
        cooperativeUserIdSql = "SELECT id FROM cooperative_user WHERE cooperative_account ='" + self.cooperativeAccount + "'"
        cooperativeUserId = db().select(cooperativeUserIdSql)
        self.add_activation(cooperativeUserId)
        time.sleep(1)
        activationIdSql = "SELECT id FROM cooperative_activation WHERE cooperativeUser_id ={}".format(cooperativeUserId)
        activationId = db().select(activationIdSql)
        self.pro_activation(cooperativeUserId, activationId)
        time.sleep(1)
        activationCode = self.getCodeDetail(activationId)

        '''检查激活码-获取pomp验证码-校验pomp验证码-登陆pomp-登陆检查'''


        '''新增停车场'''

        return activationId, activationCode


if __name__ == '__main__':
    userAccount = "test{}".format(SuperAction().get_time())
    a = aomp()
    activationId, activationCode = a.main()
    p = Operation_parking()
    p.validateActivationCode(activationCode)
    p.validUser(userAccount)
    print("userAccount", userAccount)
    p.registerUser(activationCode, userAccount)
    p = pomp(userAccount)
    time.sleep(1)
    c = CreateParking(p.userAccount).newParking(activationCode)
    print(c.text)


