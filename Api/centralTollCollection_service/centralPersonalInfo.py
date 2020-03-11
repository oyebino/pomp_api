"""
 Created by lgc on 2020/3/11 15:15.
 微信公众号：泉头活水
"""

from common.Req import Req

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}

class CentralPersonalInfo(Req):
    """个人中心"""

    def duty_info(self):

        """个人信息"""
        self.url = "/ydtp-backend-service/api/central/duty_info"
        re = self.get(url=self.zby_api, headers=form_headers)
        return re