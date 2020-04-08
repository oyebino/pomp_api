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
        return re.json()

    def handOverCentralDuty(self, user, pwd):
        """中央收费处交接班"""
        self.url = "/ydtp-backend-service/api/hand_over_central_duty"
        data = {
            "user_id": user,
            "password": pwd
        }
        re = self.post(self.zby_api, data=data, headers =form_headers)
        return re.json()

    def centralOffDuty(self):
        """中央收费处下班"""
        self.url = "/ydtp-backend-service/api/central_off_duty"
        re = self.post(self.zby_api, headers = form_headers)
        return re.text

