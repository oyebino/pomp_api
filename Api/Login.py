# -*- coding: utf-8 -*-
# @File  : parkVisitorlist.py
# @Author: 叶永彬
# @Date  : 2019/11/16
# @Desc  :

from Config.Config import Config
from urllib.parse import urljoin
from common.logger import logger as log
from urllib.parse import urlencode
import requests
from Config.parameter import LoginReponse
from common.superAction import SuperAction as SA

json_headers = {"Content-Type": "application/json;charset=UTF-8"}
form_headers = {"content-type": "application/x-www-form-urlencoded"}

class Login():
    def __init__(self,user=None,pwd=None):
        self.conf = Config()
        self.host = self.conf.host
        self.Seesion = requests.Session()
        if user == None and pwd == None:
            self.user = Config().getValue("user")
            self.password = Config().getValue("password")
        else:
            self.user = user
            self.password =pwd

    def login(self):
        seccode = urljoin(self.host,"/mgr/normal/authz/seccode.do")
        verify_seccode = urljoin(self.host,"/mgr/normal/authz/verify_seccode.do")
        url = urljoin(self.host,"/mgr/normal/ajax/login.do")
        headers ={
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
        re = self.Seesion.get(seccode,headers = headers)
        data = {"seccode": 9999}
        re = self.Seesion.post(verify_seccode,data=data)
        data = {
            "username": self.user,
            "password": self.password,
            "seccode": 9999
        }
        login = self.Seesion.post(url,data)
        LoginReponse.loginRe = login
        loginDict = login.json()['data']
        try:
            payload = {
                "id": loginDict['id'],
                "loginid": loginDict['loginid'],
                "nickname": loginDict['nickname'],
                "mobile": loginDict['mobile'],
                "email": loginDict['email'],
                "operatorID": loginDict['operatorID'],
                "address": loginDict['address'],
                "isMockLogin": loginDict['isMockLogin'],
                "operatorIDList[]": loginDict['operatorIDList'][0],
                "topOperatorId": loginDict['topOperatorId']
            }
            executeUrl = self.host + '/mgr/zbcloud-grey/api/execute?'
            executeApi = executeUrl + urlencode(payload)
            re = self.Seesion.get(executeApi)
            if re.text =='ok':
                log.info("用户【" +data['username'] + "】" + login.json()['message'])
                return self.Seesion
        except TypeError:
            return self.Seesion

from Api.parkingManage_service.tollCollection import TollCollection as Tol
import json
class SentryLogin():
    """岗亭端"""

    def __init__(self,user = None, pwd = None):
        self.S = requests.Session()
        self.C = Config()
        self.host = self.C.zby_host
        if user == None and pwd == None:
            self.user = self.C.zby_user
            self.password = self.C.zby_pwd
        else:
            self.user = user
            self.password = pwd

    def login(self):
        """登录并获取token"""
        # self.__forceofDutyAllUser()
        url = self.host + "/user-service/api/sessions"
        data = {
            "user_id": self.user,
            "password": self.password
        }
        self.S.headers.update({"cookie":"akeparking_grey_zone_name = grey"})
        loginRe = self.S.post(url=url, data=data, headers=form_headers)
        LoginReponse.loginRe = loginRe
        try:
            login = loginRe.json()
            token = login['token']
            self.S.headers.update({"user": token,"type": "ydtp-pc"})
            executeUrl = self.host + '/ydtp-backend-service/zbcloud-grey/api/execute?'
            executeApi = executeUrl + urlencode({"topOperatorId": login['topOperatorId']})
            re = self.S.get(executeApi,)
            if re.text == 'ok':
                log.info("登录名：【"+data['user_id']+"】")
                if login['onDuty'] == 0:
                    self.__selectChannel()
                return self.S
        except KeyError:
            return self.S

    def __forceofDutyAllUser(self):
        """强制下班所有用户"""
        idList = []
        try:
            userList = Tol(Login().login()).getAllTollCollection('上班中')
            for user in userList:
                idList.append(user['id'])
            for id in idList:
                Tol(Login().login()).forceOfDuty(id)
        except json.JSONDecodeError:
            pass


    def __getAllChannel(self):
        """获取当前用户的全部通道"""
        url = self.host + "/ydtp-backend-service/api/sentry_user_parking"
        re = self.S.get(url=url)
        channelList = []
        parkList = re.json()
        for park in parkList:
            for channelDict in park['channels']:
                channelList.append(channelDict['id'])
        return channelList

    def __selectChannel(self):
        """选择通道上班"""
        url = self.host + "/ydtp-backend-service/api/duty"
        channelCodeList = self.__getAllChannel()
        data = {
            "channel_ids": channelCodeList
        }
        r = self.S.post(url=url, data=data)

class CenterMonitorLogin():

    """远程值班"""
    def __init__(self,user = None, pwd = None):
        self.S = requests.Session()
        self.host = Config().host
        self.mock_host = Config().mock_host
        if user == None and pwd == None:
            self.user = Config().getValue("user")
            self.password = Config().getValue("password")
        else:
            self.user = user
            self.password = pwd

    def login(self):

        """校验图片验证码-登陆中央值守"""
        sessionId = SA().get_time()
        url = self.host + "/zbcloud/user-service/cenduty/seat/getVerificationCode?sessionId={}".format(sessionId)
        self.S.get(url=url)
        url = self.host + "/zbcloud/user-service/cenduty/seat/login"
        data = {
                "userid": "{}".format(self.user),
                "password": self.__setPwd(self.password),
                "validateCode": "9999",
                "sessionId": "{}".format(sessionId)
                }
        log.info("登录名：【"+data['userid']+"】")
        r = self.S.post(url=url, json=data, headers=json_headers)
        LoginReponse.loginRe = r
        if r.json()['status'] == 0:
            token = r.json()['message'].split(";")[0]
            topOperatorId = r.json()['message'].split(";")[-1]
            self.S.headers.update({"token": token})
            websocketUrl = "wss://monitor.k8s.yidianting.com.cn/zbcloud/center-monitor/websocket"
            print((self.__createUserSocket(websocketUrl,token)).json())
            executeUrl = self.host + '/zbcloud/center-monitor-service/zbcloud-grey/api/execute?topOperatorId={}'.format(topOperatorId)
            re = self.S.get(executeUrl, headers = form_headers)
            if re.text == 'ok':
                return self.S
        else:
            return self.S

    def __createUserSocket(self, ip ,token):
        """请求创建用户的socket"""
        data = {
            "message_id": SA().get_uuid(),
            "timestamp": SA().get_time(),
            "biz_content":{
                "login_url": ip,
                "login_token": token
            }
        }
        url = self.mock_host + "/mock_login_center_monitor"
        re = self.S.post(url, json=data, headers = json_headers)
        return re


    def __setPwd(self,pwd):
        """md5密码加密"""
        import hashlib
        m = hashlib.md5()
        b = str(pwd).encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        return str_md5

class AompLogin(object):
    """Aomp,不需要灰度用户，只在ip连接加个grey就可以"""
    def __init__(self, user = None, pwd = None):
        self.conf = Config()
        self.host = self.conf.aomp_host
        self.Session = requests.session()
        if user == None and pwd == None:
            self.user = self.conf.aomp_user
            self.password = self.conf.aomp_pwd
        else:
            self.user = user
            self.password = pwd

    def login(self):
        """"校验验证码"""
        loginUrl = self.host + "/checkLogin.do"
        data = {
            "user": "{}".format(self.user),
            "pwd": "{}".format(self.password),
            "validateCode": "9999",
            "isOnLine": "isOnLine",
            "flag": "-1"
        }
        loginRe = self.Session.post(loginUrl, data)
        LoginReponse.loginRe = loginRe
        return self.Session


class WeiXinLogin():

    """微信商户端"""
    def __init__(self,user = None, pwd = None):
        self.conf = Config()
        self.host = self.conf.weiXin_host
        self.S = requests.session()
        if user == None and pwd == None:
            self.user = self.conf.weiXin_user
            self.password = self.conf.weiXin_pwd
        else:
            self.user = user
            self.password = pwd

    def login(self):
        loginUrl = self.host + "/mgr-weixin/passport/signin.do"
        data = {
            "username": self.user,
            "password": self.password
        }
        print(data['username'])
        loginRe =self.S.post(loginUrl, data)
        LoginReponse.loginRe = loginRe
        return self.S

class OpenYDTLogin():
    """开放平台"""
    def __init__(self):
        self.S = requests.session()

    def login(self):
        import base64
        import time
        from Config.parameter import tempDataPath
        time_tup = time.localtime(time.time())
        format_time = '%Y%m%d%H%M%S'
        cur_time = time.strftime(format_time, time_tup)
        tempDataPath.cur_time = cur_time
        authorization_str = b'test:' + cur_time.encode('utf-8')
        authorization = base64.b64encode(authorization_str)
        print(authorization)
        self.S.headers.update({"Authorization":authorization})
        return self.S

class CentralTollLogin():

    """中央收费登陆"""
    def __init__(self, zby_user=None, zby_pwd=None):
        self.S = requests.Session()
        self.host = Config().zby_host
        if zby_user == None and zby_pwd == None:
            self.user = Config().getValue("zby_user")
            self.password = Config().getValue("zby_pwd")
        else:
            self.user = zby_user
            self.password = zby_pwd

    def login(self):

        """登陆中央收费页面"""
        url = self.host + "/ydtp-backend-service/api/open/central_duty"
        data = {
                "user_id": "{}".format(self.user),
                "password": "{}".format(self.password)
                }
        print("登录名：【"+data['user_id']+"】")
        print("密码：【" + data['password'] + "】")
        self.S.headers.update({"cookie":"akeparking_grey_zone_name=grey"})
        r = self.S.post(url=url, data=data, headers=form_headers)
        LoginReponse.loginRe = r
        try:
            token = r.json()['token']
            topOperatorId = r.json()['topOperatorId']
            self.S.headers.update({"user": token, "type": "ydtp"})
            executeUrl = self.host + "/ydtp-backend-service/zbcloud-grey/api/execute?topOperatorId={}".format(topOperatorId)
            re = self.S.get(executeUrl, headers = form_headers)
            if re.text == 'ok':
                return self.S
        except KeyError:
            return self.S

class RoadSideLogin():
    """路边登录"""
    def __init__(self,user = None,pwd = None):
        self.S = requests.Session()
        self.host = Config().roadSide_host
        if user == None and pwd == None:
            self.user = Config().getValue("roadSide_user")
            self.password = Config().getValue("roadSide_pwd")
        else:
            self.user = user
            self.password = pwd

    def login(self):
        url = self.host + "/parking/checkLogin.do"
        data = {
            "user": self.user,
            "cipher": self.password,
            "isOnLine": "isOnLine",
            "flag":3
        }
        r = self.S.post(url=url, data=data, headers=form_headers)
        LoginReponse.loginRe = r
        print(r.json())
        return self.S



if __name__ == "__main__":

    L = CenterMonitorLogin()
    # ip ="wss://monitor.k8s.yidianting.com.cn/zbcloud/center-monitor/websocket"
    L.login()
    # re =L.createUserSocket(ip,'123456')
    # print(re.json())


