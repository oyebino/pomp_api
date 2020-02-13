"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
import requests

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}


class CheckInOut():
    """
    pc收费端相关业务
    """
    def __init__(self, host="https://zbcloud.k8s.yidianting.com.cn"):
        self.S = requests.Session()
        self.host = host

    def check_message_in_out(self,token):
        """
        获取所有消息并提取最新id
        """
        url = self.host + "/ydtp-backend-service/api/messages?type=undeal&pageNumber=1&pageSize=250"
        form_headers['user'] = token
        form_headers['type'] = 'ydtp-pc'
        re = self.S.get(url, headers=form_headers)
        print("消息：",re.json())
        messageList = re.json()['list']
        print("messagelist****", messageList)
        if len(messageList) != 0:
            id = re.json()["list"][0]["id"]
            return id
        else:
            return None

    def check_car_in_out(self,id):
        """
        点击消息，然后点击确认放行
        """
        url = self.host + "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "确认放行",
            "reason": ""
        }
        print(url)
        re = self.S.post(url, data=data, headers=form_headers)
        return re.json()

    def normal_car_out(self,id):
        """
        点击收费放行
        """
        url = self.host + "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "收费放行",
            "reason": ""
        }
        print(url)
        re = self.S.post(url, data=data, headers=form_headers)
        print(re.text)
        return re.text

    def abnormal_car_out(self, id):
        """
        异常放行
        """
        url = self.host + "/ydtp-backend-service/api/messages/{}/go".format(id)
        data = {
            "type": "异常放行",
            "reason": "",
            "real_value": "1"
        }
        print(url)
        re = self.S.post(url, data=data, headers=form_headers)
        print(re.text)
        return re.text

if __name__ == "__main__":
    s =CheckInOut()
    id = s.check_message_in_out("3c18676172552306aed17d9853c1263e")
    s.check_car_in_out(id)