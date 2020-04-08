#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/31 9:28
# @Author  : 叶永彬
# @File    : cendutySeat.py

from common.Req import Req
from common.superAction import SuperAction as SA
from urllib.parse import urlencode
from Api.index_service.index import Index

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CendutySeat(Req):
    """远程值班帐号管理"""

    def cendutySeatList(self, username = None, onlineStatus = '全部'):
        """远程值班账号列表"""
        onlineStatusDict = {'全部':None, '离开':2, '休息中':0, '上班中':1 }
        operatorId = Index(self.Session).getNewMeun().json()['user']['operatorID']
        data = {
            "onlineStatus": onlineStatusDict[onlineStatus],
            "operatorId": operatorId,
            "pageNumber": 1,
            "pageSize": 20,
            "username": username
        }
        self.url = "/mgr/cenduty/seat/list"
        re = self.post(self.api, json= data, headers = json_headers)
        return re.json()['data']['list']

    def __getOperatorParkList(self, operatorId):
        """获取当前用户权限停车场"""
        data = {
           "operatorId":  operatorId
        }
        self.url ="/mgr/cenduty/seat/getOperatorParkList?" + urlencode(data)
        re = self.get(self.api, headers = form_headers)
        return re

    def addCendutySeat(self, userId, username, pwd):
        """新增远程值班账号"""
        operatorDict = Index(self.Session).getNewMeun().json()['user']
        parkList = self.__getOperatorParkList(operatorDict['operatorID']).json()['data']
        data = {
            "createBy": operatorDict['nickname'],
            "des": "",
            "operatorId": operatorDict['operatorID'],
            "parkList": parkList,
            "password": pwd,
            "speaker": 1,
            "userid": userId,
            "username": username,
            "userphone": "135{}".format(SA().create_randomNum(val=8))
        }
        self.url = "/mgr/cenduty/seat/add"
        re = self.post(self.api, json = data, headers= json_headers)
        return re.json()

    def updateCendutySeat(self,userId, username = None, pwd = None):
        """
        修改远程值班账号
        :param userid: 登录账号
        :param username: 登录名称
        :param pwd:
        :return:
        """
        userDict = self.getDictBykey(self.cendutySeatList(), 'userid', userId)
        parkList = self.__getBindParkList(userDict['id']).json()['data']
        operatorDict = Index(self.Session).getNewMeun().json()['user']
        if username == None:
            username = userDict['username']
        data = {
            "des": "",
            "id": userDict['id'],
            "operatorId": operatorDict['operatorID'],
            "parkList": parkList,
            "password": pwd,
            "speaker": userDict['speaker'],
            "updateBy": operatorDict['nickname'],
            "userid": userDict['userid'],
            "username": username,
            "userphone": userDict['userphone']
        }
        self.url = "/mgr/cenduty/seat/update"
        re = self.post(self.api, json= data, headers = json_headers)
        return re.json()

    def __getBindParkList(self, userListId):
        """获取绑定车场列表"""
        data = {
            "id": userListId
        }
        self.url = "/mgr/cenduty/seat/getBindParkList?" + urlencode(data)
        re = self.get(self.api)
        return re

    def lockCendutySeat(self, userId):
        """冻结远程值班账号"""
        userDict = self.getDictBykey(self.cendutySeatList(), 'userid', userId)
        data = {
            "id": userDict['id']
        }
        self.url = "/mgr/cenduty/seat/lock?" + urlencode(data)
        re = self.post(self.api, headers = form_headers)
        return re.json()

    def startCendutySeat(self,userId):
        """开启远程值班账号"""
        userDict = self.getDictBykey(self.cendutySeatList(), 'userid', userId)
        data = {
            "id": userDict['id']
        }
        self.url = "/mgr/cenduty/seat/start?" + urlencode(data)
        re = self.post(self.api, headers = form_headers)
        return re.json()

    def deleteCendutySeat(self,userId):
        """删除远程值班账号"""
        userDict = self.getDictBykey(self.cendutySeatList(), 'userid', userId)
        data = {
            "id": userDict['id']
        }
        self.url = "/mgr/cenduty/seat/delete?" + urlencode(data)
        re = self.post(self.api, headers = form_headers)
        return re.json()






