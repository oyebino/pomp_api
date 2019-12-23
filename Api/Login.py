# -*- coding: utf-8 -*-
# @File  : parkVisitorlist.py
# @Author: 叶永彬
# @Date  : 2019/11/16
# @Desc  :

from Config.Config import Config
from urllib.parse import urljoin
from common.logger import logger as log

import requests

import json

class Login():

    def __init__(self):

        self.conf = Config()
        self.host = self.conf.host
        self.Seesion = requests.Session()
        self.user = Config().getValue("user")
        self.password = Config().getValue("password")

    def login(self):

        seccode = urljoin(self.host,"/mgr/normal/authz/seccode.do")

        verify_seccode = urljoin(self.host,"/mgr/normal/authz/verify_seccode.do")

        url = urljoin(self.host,"/mgr/normal/ajax/login.do")


        headers ={
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        re = self.Seesion.get(seccode)

        data = {"seccode": 9999}

        re = self.Seesion.post(verify_seccode,data=data)

        data = {
            "username": self.user,
            "password": self.password,
            "seccode": 9999
        }
        re = self.Seesion.post(url,data,headers=headers)

        log.info(re.json()['message'])

        return self.Seesion



if __name__ == "__main__":

    L = Login()

    L.login()
