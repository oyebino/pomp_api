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

form_headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
json_headers = {"Content-Type": "application/json;charset=UTF-8"}

class CarInOutHandle(Req):
    """pc收费端相关业务：获取所有消息id，对消息记录确认放行、收费放行、异常放行"""
    date = SuperAction().get_today_data()
    carTypeDict = {'蓝牌车': 1, '黄牌车': 2, '新能源小车': 4, '新能源大车': 3,'': None}

    def carInOutHandle(self,carNum,carHandleType,jobId = ""):
        """
        车辆进出场处理（登记放行，收费放行，异常放行）
        :param carNum:
        :param channelName:
        :param carHandleType: '登记放行','异常放行','登记放行','确认放行'
        :param jobId:
        :return:
        """
        # channelDict = self.getDictBykey(self.__getDutyChannelStatus().json(), 'entrance_name', channelName)
        type = carHandleType.strip()
        if type == "登记放行":
            type = ""
            carHandleInfoDict = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'carNo', carNum)
        elif type == "收费放行" or "异常放行" or "确认放行":
            carHandleInfoDict = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'leaveCarNo', carNum)
        self.url = "/ydtp-backend-service/api/messages/{}/go".format(carHandleInfoDict['id'])
        data = {
            "type": type,
            "reason": "",
            "real_value":1
        }
        if type == "收费放行":
            self.save('payVal', carHandleInfoDict['content']['payVal'])
        else:
            self.save('payVal', data['real_value'])
        re = self.post(self.zby_api, data=data, headers=form_headers)
        sleep(3)  # 可能需要加上延时

        if jobId != "" and "success" in re.json() and re.json()["success"] == True:
            result = cloudparking_service().getCarMsgYtj(jobId)
            return result
        else:
            return re.json()["success"]

    def adjustCarNum(self, carNum, adjustCarNum, carType = ''):
        """进场前校正车牌与类型"""
        carInOutHandle = self.__getCarInOutHandleIdList()
        try:
            carHandleInfo = self.getDictByList(carInOutHandle, 'content', 'carNo', carNum)
        except KeyError:
            carHandleInfo = self.getDictByList(carInOutHandle, 'content', 'leaveCarNo', carNum)
        self.url = "/ydtp-backend-service/api/messages/{}/carCode".format(carHandleInfo['id'])
        data = {
            "car_code": adjustCarNum,
            "operateSource": "2",
            "carType": self.carTypeDict[carType]
        }
        re =self.post(self.zby_api,data=data,headers = form_headers)
        print(re.text)
        if re.json()['open_gate'] == False:
            re = self.getHandleIdInfo(carHandleInfo['id'])
            return re['content']
        else:
            return re.json()

    def patchRecord(self, carNum, parkName, adjustCarNum, carType = None):
        """在场车辆校正"""
        carInfoDict = self.getDictBykey(self.getCarInRecord(carNum, parkName), 'carCode', carNum)
        self.url = "/ydtp-backend-service/api/records/patch"
        data = {
            "car_code": adjustCarNum,
            "topBillCode": carInfoDict['topBillCode'],
            "modifyType":1,
            "operateSource": 2,
            "carType": carType
        }
        re = self.post(self.zby_api, data = data, headers = form_headers)
        return re.text

    def matchCarNum(self,carNum,matchCarNum):
        """人工匹配车牌"""
        carHandleInfo = self.getDictByList(self.__getCarInOutHandleIdList(), 'content', 'leaveCarNo', carNum)
        carHandleIdInfo = self.getHandleIdInfo(carHandleInfo['id'])
        matchCarInfo = self.getDictBykey(carHandleIdInfo,'car_code',matchCarNum)

        self.url = "/ydtp-backend-service/api/messages/{}/match".format(carHandleIdInfo['id'])
        data = {
            "top_bill_code": matchCarInfo['top_bill_code'],
            "area_record_code": matchCarInfo['area_record_code'],
            "park_uuid":carHandleIdInfo['park_uuid']
        }
        re = self.post(self.zby_api,data=data,headers=form_headers)
        if re.json()['open_gate'] == False:
            re = self.getHandleIdInfo(carHandleIdInfo['id']).json()
            return re['content']
        else:
            return re.json()

    def getHandleIdInfo(self,id):
        """获取处理车辆ID的信息"""
        self.url = "/ydtp-backend-service/api/messages/{}".format(id)
        re = self.get(self.zby_api,headers = json_headers)
        return re.json()

    def getCarInRecord(self,car_code, parkName, mode=''):
        """
        获取进场记录
        """
        parkDict = self.getDictBykey(self.__onDutyParks(), 'park_name', parkName)
        data ={
            "car_code":car_code,
            "park_id": parkDict['id'],
            "mode":mode,
            "pageSize": "40",
            "pageNumber": "1",
            "record_type": "in"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers=form_headers)
        return re.json()['rows']

    def getCarOutRecord(self,carNum, parkName, mode = ""):
        """
        获取出场记录
        """
        parkDict = self.getDictBykey(self.__onDutyParks(),'park_name',parkName)
        data ={
            "pageSize": "40",
            "pageNumber": "1",
            "car_code": carNum,
            "mode": mode,
            "park_id": parkDict['id'],
            "record_type": "out"
        }
        self.url = "/ydtp-backend-service/api/records?{}&begin_time={}+00:00:00&end_time={}+23:59:59".format(urlencode(data),self.date,self.date)
        re = self.get(self.zby_api, headers = form_headers)
        return re.json()['rows']

    def __onDutyParks(self):
        """当前用户上班车场"""
        self.url = "/ydtp-backend-service/api/on_duty_parks"
        re = self.get(self.zby_api, headers = json_headers)
        parkList = {'parkList': re.json()}
        return parkList

    def __getDutyChannelStatus(self):
        """获取当前用户上班通道"""
        self.url = "/ydtp-backend-service/api/duty_channel_status"
        re = self.get(self.zby_api, headers = json_headers)
        return re

    def __getCarInOutHandleIdList(self):
        """获取处理车辆进出的id块"""
        data = {
            "type": "undeal",
            "pageNumber": 1,
            "pageSize": 250
        }
        self.url = "/ydtp-backend-service/api/messages?" + urlencode(data)
        re = self.get(self.zby_api)
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