"""
 Created by lgc on 2020/2/26 15:32.
 微信公众号：泉头活水
"""

from common.Req import Req
from common.superAction import SuperAction as SA
from Api.cloudparking_service import cloudparking_service
from urllib.parse import urlencode
from Api.centerMonitor_service.personalInfo import PersonalInfo

form_headers = {"content-type": "application/x-www-form-urlencoded"}
json_headers = {"content-type": "application/json;charset=UTF-8"}

class CarInOutHandle(Req):
    """远程值班室-处理车辆"""
    date = SA().get_today_data()
    endDate = SA().cal_get_day('%Y-%m-%d',days=1)

    def checkCarIn(self, carNum):
        """远程值班室-处理车辆进场-登记放行"""
        handleCarDict = cloudparking_service()._getCenterMonitorHandleCarMsg(carNum)
        data = {
            "carInOutId": handleCarDict['carInMsg']['carInOutId'],
            "dutyMessage": handleCarDict,
            "handleMessage": "放行原因为：",
            "reason": ""
        }
        self.url = "/zbcloud/center-monitor-service/in-out/check-in"
        re = self.post(self.monitor_api, json = data, headers = json_headers)
        return re.json()

    def checkCarOut(self, carNum):
        """远程值班室-处理车辆出场-异常放行"""
        handleCarDict = cloudparking_service()._getCenterMonitorHandleCarMsg(carNum)
        data = {
            "carInOutId": handleCarDict['carOutMsg']['carInOutId'],
            "dutyMessage": handleCarDict,
            "handleMessage": "放行原因为：异常放行",
            "leaveType": 3,
            "payVal": handleCarDict['carOutMsg']['payVal'],
            "reason": ""
        }
        self.url = "/zbcloud/center-monitor-service/in-out/check-out"
        re = self.post(self.monitor_api, json = data, headers = json_headers)
        return re.json()

    def carInOutRecord(self, parkName, carNum, type, mode = '全部'):
        """远程值班室-车辆在场、出场记录"""
        modeDict = {"全部":"","自动入行": 1,"确认放行": 2,"异常放行": 3,"遥控开闸": 4,"自助开闸": 5,"可疑跟车": 6,"盘点进场": 7}
        presonalDict = PersonalInfo(self.Session).getCendutySeat()
        parkDict = self.getDictBykey({"parkList":self.__getBingParkList().json()}, 'name', parkName)
        data = {
            "park_id": parkDict['parkId'],
            "mode": modeDict[mode],
            "record_type": type,
            "car_code": carNum,
            "pageNumber": 1,
            "pageSize": 1,
            "id": presonalDict['id'],
            "begin_time": self.date + " 00:00:00",
            "end_time": self.endDate + " 23:59:59",
        }
        self.url = "/zbcloud/center-monitor-service/in-out/open/cenduty_records?" + urlencode(data)
        re = self.get(self.monitor_api, headers = form_headers)
        return re.json()['rows']

    def __getBingParkList(self):
        """获取用户绑定车场列表"""
        data = {
            "t": SA.getTimeStamp()
        }
        self.url = "/zbcloud/center-monitor-service/cenduty/seat/getBindParkList?" + urlencode(data)
        re = self.get(self.monitor_api)
        return re

    def checkMonthTicketList(self, parkName="", carNum="", ticketName = ""):
        """查看月票车辆"""
        if not parkName == "":
            parkDict = self.getDictBykey({"parkList": self.__getBingParkList().json()}, 'name', parkName)
        else:
            parkDict = {}
            parkDict['parkId'] = ""
        data = {
            "carCode":carNum,
            "pageNumber": 1,
            "pageSize": 1,
            "parkUUID": parkDict['parkId'],
            "sortType": "ASC",
            "ticketName": ticketName
        }
        self.url = "/zbcloud/center-monitor-service/vip/month-ticket/list"
        re = self.post(self.monitor_api, json= data, headers = json_headers)
        return re.json()['rows']

    def adjustCarNum(self, carNum, correctCarNum):
        """
        校正车牌
        :param carNum: 原车辆
        :param correctCarNum: 校正车辆
        :return:
        """
        handleCarDict = cloudparking_service()._getCenterMonitorHandleCarMsg(carNum)
        if handleCarDict['msg_type'] == '进车':
            carInOutId = handleCarDict['carInMsg']['carInOutId']
        elif handleCarDict['msg_type'] == '出车':
            carInOutId = handleCarDict['carOutMsg']['carInOutId']
        else:
            carInOutId = None
        data = {
            "carInOutId": carInOutId,
            "correctCarNo": correctCarNum,
            "dutyMessage": handleCarDict,
            "handleMessage": "校正车牌为：{}".format(correctCarNum)
        }
        self.url = "/zbcloud/center-monitor-service/in-out/correct-car"
        re = self.post(self.monitor_api, json= data, headers = json_headers)
        return re.json()

    def adjustCarNumByConfidenceAlarm(self, carNum, adjustCarNum):
        """进场置信度告警-校正车辆"""
        handleCarDict = cloudparking_service()._getCenterMonitorHandleCarMsg(carNum)
        data = {
            "carType": handleCarDict['carType'],
            "correctCarCode": adjustCarNum,
            "modifyType": 3,
            "topBillCode": handleCarDict['topBillCode']
        }
        self.url = "/zbcloud/center-monitor-service/car-record/correct-car-code"
        re = self.post(self.monitor_api, json= data, headers = json_headers)
        return re.json()

    def sendVoiceMessage(self, carNum, msg):
        """发送语音"""
        handleCarDict = cloudparking_service()._getCenterMonitorHandleCarMsg(carNum)
        data = {
            "channelId": handleCarDict['channelId'],
            "dutyMessage": handleCarDict,
            "handleMessage": "发送语音到一体机,内容为：{}".format(msg),
            "screen": msg,
            "voice": msg
        }
        self.url = "/zbcloud/center-monitor-service/message/send"
        re = self.post(self.monitor_api, json = data, headers= json_headers)
        return re.json()