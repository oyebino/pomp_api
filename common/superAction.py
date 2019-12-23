#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 15:41
# @Author  : 叶永彬
# @File    : superAction.py
import random,string
import datetime,time
import uuid

class SuperAction:

    def create_carNum(self, uppercase_num=1, digits_num=5, carType=None):
        """创建随机车牌"""
        ascii_uppercase = 'ABCDEGHJKLMNPQRSTWXY'
        src_digits = string.digits  # string_数字
        src_uppercase = ascii_uppercase  # string_大写字母
        # 生成字符串
        carNum = random.sample(src_uppercase, uppercase_num) + random.sample(src_digits, digits_num)
        # 列表转字符串
        if carType == "民航":
            new_carNum = "民航" + ''.join(carNum)[1:]
        elif carType == "新能源":
            new_carNum = "粤" + ''.join(carNum) + "F"
        else:
            new_carNum = "粤" + ''.join(carNum)
        return new_carNum

    def get_time(self,strType = "%Y%m%d%H%M%S"):
        dt = datetime.datetime.now()
        return dt.strftime(strType)

    def get_today_data(self):
        dt = datetime.date.today()
        return str(dt)

    def get_utcTime(self,strType="%Y-%m-%dT%H:%M:%S.001Z"):
        now = datetime.datetime.now()
        date = now - datetime.timedelta(seconds= 28800)
        return date.strftime(strType)

    def cal_get_utcTime(self,strType="%Y-%m-%dT%H:%M:%S.001Z",second=60,style = "+"):
        now = datetime.datetime.now()
        if style=="+":
            date = now - datetime.timedelta(seconds=28800) + datetime.timedelta(seconds=second)
        else:
            date = now - datetime.timedelta(seconds=28800) - datetime.timedelta(seconds=second)
        return date.strftime(strType)

    def cal_get_time(self,strType ="%Y%m%d%H%M%S", seconds = 1, style ="+"):
        now = datetime.datetime.now()
        if style=="+":
            date = now + datetime.timedelta(seconds = seconds)
        else:
            date = now - datetime.timedelta(seconds=seconds)
        return date.strftime(strType)

    def cal_get_day(self,strType ="%Y%m%d", days = 1, style ="+"):
        now = datetime.date.today()
        if style=="+":
            date = now + datetime.timedelta(days = days)
        else:
            date = now - datetime.timedelta(days = days)
        return date.strftime(strType)

    def get_uuid(self):
        uuidlist = str(uuid.uuid1()).split("-")
        newstr = ""
        for i in range(1, len(uuidlist)):
            newstr += uuidlist[i]
        return newstr

    def save_data(self):
        """
        保存案例的运行时的数值
        :return:
        """

    def create_random_name(self):
        src_digits = string.digits
        name= "月票"+"".join(random.sample(src_digits, 4))
        return name

    def create_randomNum(self,val= 4):
        src_digits = string.digits
        value = "".join(random.sample(src_digits, val))
        return value

    def changeDate(self,json):
        """
        深度把json数据体具有unicode转换成中文
        :param json:
        :return:
        """
        for key in json.keys():
            typeName = type(json.get(key))
            if typeName == list:
                for lister in json.get(key):
                    self.changeDate(lister)
            elif typeName == dict:
                self.changeDate(json.get(key))
            elif typeName == str:
                json.get(key).encode()
        return json

    # 获取当前时间的自然月
    def get_now_natural_month(self):
        import calendar
        import datetime
        today = datetime.datetime.today()
        now_month = '%s-%s' % (today.year, today.month)
        monthRange = calendar.monthrange(today.year, today.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(now_month, now_month, monthRange)
        return timeperiodListStr

    # 获取当前时间的下个月的自然月
    def get_next_natural_month(self):
        import calendar
        import datetime
        from dateutil.relativedelta import relativedelta
        next_month_day = datetime.date.today() - relativedelta(months=-1)
        next_nonth = '%s-%s' % (next_month_day.year, next_month_day.month)
        monthRange = calendar.monthrange(next_month_day.year, next_month_day.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(next_nonth, next_nonth, monthRange)
        return timeperiodListStr

    # 获取当前时间的两个月的自然月
    def get_two_natural_month(self):
        import calendar
        import datetime
        from dateutil.relativedelta import relativedelta
        today = datetime.datetime.today()
        now_month = '%s-%s' % (today.year, today.month)
        next_month_day = datetime.date.today() - relativedelta(months=-1)
        next_nonth = '%s-%s' % (next_month_day.year, next_month_day.month)
        monthRange = calendar.monthrange(next_month_day.year, next_month_day.month)[1]
        timeperiodListStr = "{}-01 00:00:00 - {}-{} 23:59:59".format(now_month, next_nonth, monthRange)
        return timeperiodListStr

    # 获取当前时间格式为："%Y-%m-%d %H:%M:%S"
    def get_now_time(self, strType="%Y-%m-%d %H:%M:%S"):
        dt = datetime.datetime.now()
        return dt.strftime(strType)


if __name__ == "__main__":
    print(SuperAction().cal_get_day(strType = "%Y-%m-%d")+" 00:00:00")
