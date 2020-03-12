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

    def add_tollCollection(self, userId, pwd):
        """
        新增收费员-需绑定车场！！！
        """
        self.url = "/mgr/user/sentryuser/add"
        json_data = {
                        "nickName": "{}".format(self.nickName),
                        "role": "0",
                        "telephone": "18000000000",
                        "id": None,
                        "userId": "{}".format(userId),
                        "password": "{}".format(pwd)
                  }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        allNameDict = self.getDictBykey(self.__queryAllTollCollection().json(), 'nickName', self.nickName)
        id = allNameDict['id']
        self.__bind_park(id)  # 绑定车场
        return re

    def modify_tollCollection(self, editUserId, editPwd):
        """
        修改收费员
        """
        allNameDict = self.getDictBykey(self.__queryAllTollCollection().json(), 'nickName', self.nickName)
        id = allNameDict['id']
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
        return re

    def freeze_tollCollection(self):
        """
        冻结收费员
        """
        allNameDict = self.getDictBykey(self.__queryAllTollCollection().json(), 'nickName', self.nickName)
        id = allNameDict['id']
        self.url = "/mgr/user/sentryuser/freeze/{}".format(id)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def del_tollCollection(self):
        """
        冻结收费员
        """
        allNameDict = self.getDictBykey(self.__queryAllTollCollection().json(), 'nickName', self.nickName)
        id = allNameDict['id']
        self.url = "/mgr/user/sentryuser/delete/{}".format(id)
        re = self.get(self.api, headers=self.api_headers)
        return re

    def __queryAllTollCollection(self):
        self.url = "/mgr/user/sentryuser/getAll"
        json_data = {
                        "pageNumber": 1,
                        "pageSize": 250,
                        "sortType": "ASC"  # 取最新的，需排序
                    }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re

    def __bind_park(self, id):
        """
        绑定全部车场
        """
        parksList = self.__getAllParks().json()['parks']
        self.url = "/mgr/user/sentryuser/bindUserPark"
        json_data = {
                        "id": id,
                        "listParkId": parksList
                    }
        re = self.post(self.api, json=json_data, headers=self.api_headers)
        return re

    def __getAllParks(self):

        """获取所有车场-但实际上只有两个车场？"""
        self.url = "/mgr/main/getParks.do"
        re = self.post(self.api, headers=self.api_headers)
        return re

if __name__ == '__main__':
    re = TollCollection().add_tollCollection("test006")
    print(re.text)