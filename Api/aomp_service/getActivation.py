"""
 Created by lgc on 2019/12/24 16:01.
 微信公众号：泉头活水
"""
import json

from Api.Login import AompLogin
from common.Req import Req
from common.db import Db
from common.superAction import SuperAction

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class ActivationInfo(Req):

    # cooperativeAccount = 'test'+SuperAction().get_time()

    def add_cooperative_user(self, cooperativeAccount):
        """添加合作商"""
        self.url = "/cooperativeUser/saveCooperativeUser.do"
        data = {
            "cooperativeName": "test合作商{}".format(SuperAction().get_time()),
            "cooperativeAccount": "{}".format(cooperativeAccount),
            "cooperativePassword": "999999",
            "isOkPassword": "999999",
            "weixinAccountId": "2"
        }

        self.post(self.aomp_api, data=data, headers=form_headers)

    def get_activation(self, cooperativeAccount):

        """新增激活码"""
        sql = "SELECT id FROM cooperative_user WHERE cooperative_account = '{}' ORDER BY id DESC".format(cooperativeAccount)
        cooperativeUserId = Db().select(sql)
        self.url = "/cooperativeCode/addCooperativeActivation.do"
        data = {
            "cooperativeUserId": "{}".format(cooperativeUserId),
            "codeTotal": "10"
        }
        self.post(url=self.aomp_api, data=data, headers=form_headers)

        """生成激活码"""
        sql = "SELECT id FROM cooperative_activation WHERE cooperativeUser_id = '{}'".format(cooperativeUserId)
        activationId = Db().select(sql)
        self.url = "/cooperativeCode/produceCode.do"
        data = {
            "cooperativeUserId": "{}".format(cooperativeUserId),
            "activationId": "{}".format(activationId)
        }
        self.post(url=self.aomp_api, data=data, headers=form_headers)

        """获取激活码"""
        self.url = "/cooperativeCode/getCodeDetail.do"
        data = {
            "page": 1,
            "rows": "10",
            "activationId": "{}".format(activationId)
        }
        r = self.post(url=self.aomp_api, data=data, headers=form_headers).json()
        return r['rows'][0]['activationCode']


if __name__ == '__main__':
    a = AompLogin()

