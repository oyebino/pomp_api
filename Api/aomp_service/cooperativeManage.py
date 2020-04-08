"""
 Created by lgc on 2019/12/24 16:01.
 微信公众号：泉头活水
"""
from Api.Login import AompLogin
from common.Req import Req
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

class CooperativeManage(Req):
    """apmp的合作商管理"""
    def getCooperativeCode(self,cooperativeName):
        """获取未被使用的激活码"""
        # keyDetailDict = self.getDictBykey(self.__getCreateParkingKeyList(cooperativeName).json(), 'isRegister', 0)
        keyList = self.__getCreateParkingKeyList(cooperativeName).json()['rows']
        for key in keyList:
            if key['isOnline'] == 0 and key['isRegister'] == 0:
                return key['activationCode']
        print("【{}】没有可用激活！".format(cooperativeName))


    def __getCreateParkingKeyList(self,cooperativeName):
        """获取合用商激活码列表"""
        activationDict = self.getDictBykey(self.__getCooperativeCodeRecord(cooperativeName).json(),'cooperativeName',cooperativeName)
        data = {
            "page": 1,
            "rows": 1000,
            "activationId": activationDict['id']
        }
        self.url = "/cooperativeCode/getCodeDetail.do?"+ urlencode(data)
        re = self.get(self.aomp_api )
        return re

    def __getCooperativeCodeRecord(self, cooperativeName):
        """合作商列表"""
        data = {
            "page": 1,
            "rows": 1,
            "query_cooperativeName": cooperativeName
        }
        self.url = "/cooperativeCode/getCodeData.do?" + urlencode(data)
        re = self.get(self.aomp_api )
        return re

    def __getParkAuditingDataRecord(self, parkName):
        """车场基础信息记录列表"""
        data = {
            "page":1,
            "rows": 5,
            "query_name": parkName,
            "query_parkStatus": '',
        }
        self.url = "/parkAuditing/getParkAuditingData.do?" + urlencode(data)
        re = self.get(self.aomp_api)
        return re

    def saveParkAuditing(self, parkName):
        """车场信息审核"""
        parkDict = self.getDictBykey(self.__getParkAuditingDataRecord(parkName).json(), 'parkName',parkName)
        data = {
            "parkStatus": 1,
            "remark": '同意',
            "id": parkDict['id'],
            "parkId": parkDict['parkId'],
        }
        self.url = "/parkAuditing/saveParkAuditing.do"
        re = self.post(self.aomp_api, data = data, headers = form_headers)
        return re.json()






    # def add_cooperative_user(self, cooperativeAccount):
    #     """添加合作商"""
    #     self.url = "/cooperativeUser/saveCooperativeUser.do"
    #     data = {
    #         "cooperativeName": "test合作商{}".format(SuperAction().get_time()),
    #         "cooperativeAccount": "{}".format(cooperativeAccount),
    #         "cooperativePassword": "999999",
    #         "isOkPassword": "999999",
    #         "weixinAccountId": "2"
    #     }
    #
    #     self.post(self.aomp_api, data=data, headers=form_headers)
    #
    # def get_activation(self, cooperativeAccount):
    #
    #     """新增激活码"""
    #     sql = "SELECT id FROM cooperative_user WHERE cooperative_account = '{}' ORDER BY id DESC".format(cooperativeAccount)
    #     cooperativeUserId = Db().select(sql)
    #     self.url = "/cooperativeCode/addCooperativeActivation.do"
    #     data = {
    #         "cooperativeUserId": "{}".format(cooperativeUserId),
    #         "codeTotal": "10"
    #     }
    #     self.post(url=self.aomp_api, data=data, headers=form_headers)
    #
    #     """生成激活码"""
    #     sql = "SELECT id FROM cooperative_activation WHERE cooperativeUser_id = '{}'".format(cooperativeUserId)
    #     activationId = Db().select(sql)
    #     self.url = "/cooperativeCode/produceCode.do"
    #     data = {
    #         "cooperativeUserId": "{}".format(cooperativeUserId),
    #         "activationId": "{}".format(activationId)
    #     }
    #     self.post(url=self.aomp_api, data=data, headers=form_headers)
    #
    #     """获取激活码"""
    #     self.url = "/cooperativeCode/getCodeDetail.do"
    #     data = {
    #         "page": 1,
    #         "rows": "10",
    #         "activationId": "{}".format(activationId)
    #     }
    #     r = self.post(url=self.aomp_api, data=data, headers=form_headers).json()
    #     return r['rows'][0]['activationCode']


if __name__ == '__main__':
    a = AompLogin()

