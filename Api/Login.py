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

json_headers = {"Content-Type": "application/json;charset=UTF-8"}
form_headers = {"content-type": "application/x-www-form-urlencoded"}

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

class SentryLogin():
    """岗亭端"""
    def __init__(self, host="https://zbcloud.k8s.yidianting.com.cn"):
        self.S = requests.Session()
        self.host = host
        self.user = Config().getValue("user")
        self.password = Config().getValue("password")

    def login(self):
        """登录并获取token"""
        url = self.host + "/user-service/api/sessions"
        data = {
            "user_id": self.user,
            "password": self.password
        }
        r = self.S.post(url=url, data=data, headers=form_headers).json()
        token = r['token']
        self.S.headers.update({"user":token,"type":"ydtp-pc"})
        if r['onDuty'] == 0:
            self.__select_channel()
        return self.S

    def __get_allChannel(self):
        """获取当前用户的全部通道"""
        url = self.host + "/ydtp-backend-service/api/sentry_user_parking"
        re = self.S.get(url=url)
        channelList = []
        channelInfoList = re.json()[0]['channels']
        for channelDict in channelInfoList:
            channelList.append(channelDict['id'])
        return channelList

    def __select_channel(self):
        """选择通道上班"""
        url = self.host + "/ydtp-backend-service/api/duty"
        channelCodeList = self.__get_allChannel()
        data = {
            "channel_ids": channelCodeList
        }
        r = self.S.post(url=url, data=data)
        if not r.json()['status'] == 200:
            log.info(r.json()['message'])

    # def quit(self):
    #     """退出登录"""
    #     url = self.host + "/ydtp-backend-service/api/offduty"
    #     form_headers['user'] = self.token
    #     form_headers['type'] = 'ydtp-pc'
    #     self.S.post(url=url, headers=form_headers)
    #
    # def status(self):
    #     """登录或退出检查点"""
    #     url = self.host + "/ydtp-backend-service/api/duty_channel_status"
    #     form_headers['user'] = self.token
    #     form_headers['type'] = 'ydtp-pc'
    #     r = self.S.get(url=url, headers=form_headers)
    #     r_json = r.json()
    #     print(r_json)
    #     if 'message' in r_json:  # 未登录时返回的json有带message，已登录则没有
    #         return "未登录"
    #     else:
    #         return "已登录"
if __name__ == "__main__":

    L = SentryLogin()

    L.login()


