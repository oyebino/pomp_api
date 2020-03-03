"""
 Created by lgc on 2020/2/7 11:24.
 微信公众号：泉头活水
"""
import json
from time import sleep
from Api.cloudparking_service import cloudparking_service
from common.Req import Req
from common.superAction import SuperAction
from urllib.parse import urlencode

form_headers = {"Content-Type": "application/x-www-form-urlencoded"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class CarInOutHandle(Req):
    """pc收费端相关业务：获取所有消息id，对消息记录确认放行、收费放行、异常放行"""
    date = SuperAction().get_today_data()

    def carInOutHandle(self,carNum,type,jobId = ""):
        """
        车辆进出场处理（登记放行，收费放行，异常放行）
        :param carNum:
        :param channelName:
        :param type:登录放行为空，type='收费放行'，type='异常放行'
        :param jobId:
        :return:
        """
        # channelDict = self.getDictBykey(self.__getDutyChannelStatus().json(), 'entrance_name', channelName)
        type = type.strip()
        if type == "登记放行":
            type = ""
            carHandleInfoDict = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'carNo', carNum)
        elif type == "收费放行" or "异常放行":
            carHandleInfoDict = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'leaveCarNo', carNum)
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(carHandleInfoDict['id'])
        data = {
            "type": type,
            "reason": "",
            "real_value":1
        }
        if type == "收费放行":
            self.save('payVal', carHandleInfoDict['payVal'])
        else:
            self.save('payVal', data['real_value'])
        re = self.post(self.zby_api, data=data, headers=form_headers)
        sleep(3)  # 可能需要加上延时

        if jobId != "" and "success" in re.json() and re.json()["success"] == True:
            result = cloudparking_service().get_car_msg_ytj(jobId)
            return result
        else:
            return re

    # def check_car_in_out(self, carNum, channelName, jobId=""):
    #     """
    #     点击消息，然后点击确认放行
    #     """
    #     topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
    #     topBillCode = Db().select(topBillCodeSql)
    #     messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
    #     message_id = Db().select(messageIdSql)
    #
    #     self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
    #     data = {
    #         "type": "确认放行",
    #         "reason": ""
    #     }
    #     re = self.post(self.zby_api, data=data, headers=form_headers)
    #     sleep(3)  # 可能需要加上延时
    #     if jobId != "" and "success" in re.json() and re.json()["success"] == True:
    #             result = cloudparking_service().get_car_msg_ytj(jobId)
    #             return result
    #     else:
    #         return re
    #
    # def normal_car_out(self, carNum ,jobId=""):
    #     """
    #     点击收费放行
    #     """
    #     topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
    #     topBillCode = Db().select(topBillCodeSql)
    #     messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
    #     message_id = Db().select(messageIdSql)
    #
    #     self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
    #     data = {
    #         "type": "收费放行",
    #         "reason": ""
    #     }
    #     re = self.post(self.zby_api, data=data, headers=form_headers)
    #     sleep(3)  # 可能需要加上延时
    #     if jobId != "" and "success" in re.json() and re.json()["success"] == True:
    #             result = cloudparking_service().get_car_msg_ytj(jobId)
    #             return result
    #     else:
    #         return re
    #
    #
    # def abnormal_car_out(self, carNum, jobId=""):
    #     """
    #     异常放行
    #     """
    #     topBillCodeSql = "SELECT top_bill_code FROM realtime_car_in_out WHERE  car_no = '{}' ORDER BY id DESC LIMIT 1".format(carNum)
    #     topBillCode = Db().select(topBillCodeSql)
    #     messageIdSql = "SELECT id FROM park_sentry_duty_message WHERE top_bill_code = '{}' ORDER BY id DESC LIMIT 1".format(topBillCode)
    #     message_id = Db().select(messageIdSql)
    #
    #     self.url = "/ydtp-backend-service/api/messages/{}/go".format(message_id)
    #     data = {
    #         "type": "异常放行",
    #         "reason": "",
    #         "real_value": '1'
    #     }
    #     self.save('real_value',data['real_value'])
    #     re = self.post(self.zby_api, data=data, headers=form_headers)
    #     sleep(3)  # 可能需要加上延时
    #     if jobId != "" and "success" in re.json() and re.json()["success"] == True:
    #             result = cloudparking_service().get_car_msg_ytj(jobId)
    #             return result
    #     else:
    #         return re

    def adjust_carNum_carType(self, carNum, adjustCarNum, carType = None):
        """校正车牌与类型"""
        carHandleInfo = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'carNo', carNum)
        self.url = "/ydtp-backend-service/api/messages/{}/carCode".format(carHandleInfo['id'])
        data = {
            "car_code": adjustCarNum,
            "operateSource": "2",
            "carType": carType
        }
        re =self.post(self.zby_api,data=data,headers = form_headers)
        print(re.text)
        if re.json()['open_gate'] == "false":
            re = self.getHandleIdInfo(carHandleInfo['id'])
            return re
        else:
            return re

    def match_carNum(self,carNum,matchCarNum):
        """人工匹配车牌"""
        carHandleInfo = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'leaveCarNo', carNum)
        carHandleIdInfo = self.getHandleIdInfo(carHandleInfo['id']).json()
        matchCarInfo = self.getDictBykey(carHandleIdInfo,'car_code',matchCarNum)

        self.url = "/ydtp-backend-service/api/messages/{}/match".format(carHandleIdInfo['id'])
        data = {
            "top_bill_code": matchCarInfo['top_bill_code'],
            "area_record_code": matchCarInfo['area_record_code'],
            "park_uuid":carHandleIdInfo['park_uuid']
        }
        re = self.post(self.zby_api,data=data,headers=form_headers)
        if re.json()['open_gate'] == False:
            re = self.getHandleIdInfo(carHandleIdInfo['id'])
            return re
        else:
            return re

    def getHandleIdInfo(self,id):
        """获取处理车辆ID的信息"""
        self.url = "/ydtp-backend-service/api/messages/{}".format(id)
        re = self.get(self.zby_api,headers = json_headers)
        return re

    def record_car_in(self,car_code,parkId='',mode=''):
        """
        获取进场记录
        """
        data ={
            "car_code":car_code,
            "park_id": parkId,
            "mode":mode,
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "in"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers=form_headers)
        return re

    def record_car_out(self,carNum,mode = "",parkId = ""):
        """
        获取出场记录
        """

        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "car_code": carNum,
            "mode": mode,
            "park_id": parkId,
            "record_type": "out"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers=form_headers)
        return re

    def __getDutyChannelStatus(self):
        """获取当前用户上班通道"""
        self.url = "/ydtp-backend-service/api/duty_channel_status"
        re = self.get(self.zby_api,headers = json_headers)
        return re

    def __getCarInOutHandleIdList(self):
        """获取处理车辆进出的id块"""
        data = {
            "type": "undeal",
            "pageNumber": 1,
            "pageSize": 250
        }
        self.url = "/ydtp-backend-service/api/messages?" + urlencode(data)
        re = self.get(self.zby_api,headers = json_headers)
        return re.json()['list']

if __name__ == '__main__':
    # f =CarInOutHandle()
    # a = f._openGateFail()
    # print(type(a))
    # dict
    # ' object has no attribute '
    # json
    # '
    s = {'a': 5}
    print(json.dumps(s))