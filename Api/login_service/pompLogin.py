"""
 Created by lgc on 2020/1/16 13:41.
 微信公众号：泉头活水
"""
import json

import requests

from common.superAction import SuperAction


class pomp():
    """pomp url"""

    def __init__(self, userAccount, host="https://mgr.k8s.yidianting.com.cn"):
        self.S = requests.session()
        self.userAccount = userAccount
        self.host = host
        self.seccode()
        self.verify_seccode()
        self.loginPomp()

    def seccode(self):
        """获取验证码"""
        path = self.host + "/mgr/normal/authz/seccode.do"
        self.S.get(path)
        print("获取验证码----")

    def verify_seccode(self):
        """校验验证码"""
        path = self.host + "/mgr/normal/authz/verify_seccode.do"
        data = {
            "seccode": "9999"
        }
        r = self.S.post(path, data)
        print("校验验证码----", r.text)

    def loginPomp(self):
        """登陆pomp"""
        path = self.host + "/mgr/normal/ajax/login.do"
        data = {
            "username": "{}".format(self.userAccount),
            "password": "999999",
            "seccode": "9999"
        }
        r = self.S.post(path, data)
        print("login data:",data)
        print(r.text)

class Operation_parking():

    def __init__(self, host="https://mgr.k8s.yidianting.com.cn"):
        self.host = host
        self.S = requests.session()

    def validateActivationCode(self, activationCode):
        """检查激活码"""
        path = self.host + "/mgr/normal/ajax/validateActivationCode.do"
        data = {
            "code": "{}".format(activationCode)
        }
        r = self.S.post(path, data)
        print("检查激活码----")
        print(activationCode)
        print(r.text)

    def validUser(self, userAccount):
        """校验用户名"""
        path = self.host + "/mgr/normal/ajax/validUser.do"
        data = {
            "loginId": "{}".format(userAccount)
        }
        r = self.S.post(path, data)
        print("校验用户名----")
        print(r.text)
        s = json.loads(r.text)
        print(s)

    def registerUser(self, activationCode, userAccount):
        """注册运营商"""
        path = self.host + "/mgr/normal/ajax/registerUser.do"
        data = {
            "managerName": "运营商{}".format(SuperAction().get_time()),
            "userAccount": "{}".format(userAccount),
            "firstPwd": "999999",
            "confirmPwd": "999999",
            "activationCode": "{}".format(activationCode)
        }
        r = self.S.post(path, data)
        s = json.loads(r.text)
        print(s)



