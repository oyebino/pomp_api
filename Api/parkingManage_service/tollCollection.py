"""
 Created by lgc on 2020/3/12 9:18.
 微信公众号：泉头活水
"""
from common.Req import Req
from common.superAction import SuperAction


class TollCollection(Req):
    """
    收费员账号
    """
    api_headers = {"Content-Type": "application/json;charset=UTF-8"}
    nickName = "test" + SuperAction().get_time()
    roleDict = {'收费员':0, '管理员':1}
    def add_tollCollection(self, userId, pwd, role):
        """
        新增收费员-需绑定车场！！！
        """
        self.url = "/mgr/user/sentryuser/add"
        json_data = {
                        "nickName": "{}".format(self.nickName),
                        "role": self.roleDict[role],
                        "telephone": "18000000000",
                        "id": None,
                        "userId": "{}".format(userId),
                        "password": "{}".format(pwd)
                  }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re.json()

    def modify_tollCollection(self, userId, editUserId, editPwd):
        """
        修改收费员
        """
        tollNameDict = self.getDictBykey(self.getAllTollCollection(), 'userId', userId)
        id = tollNameDict['id']
        self.url = "/mgr/user/sentryuser/update"
        json_data = {
                        "nickName": "test{}".format(SuperAction().get_time()),
                        "role": "0",
                        "telephone": "18000000000",
                        "id": "{}".format(id),
                        "userId": "{}".format(editUserId),
                        "password": "{}".format(editPwd)
                  }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re.json()

    def freeze_tollCollection(self,userId):
        """
        冻结收费员
        """
        tollNameDict = self.getDictBykey(self.getAllTollCollection(), 'userId', userId)
        id = tollNameDict['id']
        self.url = "/mgr/user/sentryuser/freeze/{}".format(id)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()

    def unfreeze_tollCollection(self, userId):
        """
        解冻收费员
        """
        tollNameDict = self.getDictBykey(self.getAllTollCollection(), 'userId', userId)
        id = tollNameDict['id']
        self.url = "/mgr/user/sentryuser/unfreeze/{}".format(id)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()

    def del_tollCollection(self,userId):
        """
        删除收费员
        """
        tollNameDict = self.getDictBykey(self.getAllTollCollection(), 'userId', userId)
        id = tollNameDict['id']
        self.url = "/mgr/user/sentryuser/delete/{}".format(id)
        re = self.get(self.api, headers=self.api_headers)
        return re.json()

    def getAllTollCollection(self, dutyStatus ='全部'):
        dutyStatusDict = {'全部':None, '上班中':1, '休息中':'0'}
        self.url = "/mgr/user/sentryuser/getAll"
        json_data = {
            "pageNumber": 1,
            "pageSize": 100,
            "sortType": "ASC",  # 取最新的，需排序
            "onDuty": dutyStatusDict[dutyStatus]
        }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re.json()['list']

    def bindUserPark(self, parkName, userId):
        """
        绑定全部车场
        """
        tollNameDict = self.getDictBykey(self.getAllTollCollection(), 'userId', userId)
        parkDict = self.getDictBykey(self.__getAuthzParks().json(),'name',parkName)
        listParkId = [parkDict['uuid']]
        self.url = "/mgr/user/sentryuser/bindUserPark"
        json_data = {
                        "id": tollNameDict['id'],
                        "listParkId": listParkId
                    }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re.json()

    def __getAuthzParks(self):
        """获取所有车场-但实际上只有两个车场？"""
        self.url = "/mgr/index/getAuthzParks.do"
        re = self.get(self.api, headers=self.api_headers)
        return re

    def forceOfDuty(self, id):
        self.url = "/mgr/user/sentryuser/forceOfDuty/{}".format(id)
        re = self.get(self.api)
        return re.json()

    def forceOfDutyAll(self):
        """强制下班"""
        import json
        idList = []
        try:
            userList = self.getAllTollCollection('上班中')
            for user in userList:
                idList.append(user['id'])
            for id in idList:
                self.forceOfDuty(id)
            return "全部用户强制下班"
        except json.JSONDecodeError:
            return "全部用户强制下班"


if __name__ == '__main__':
    re = TollCollection().add_tollCollection("test006")
    print(re.text)