# -*- coding: utf-8 -*-
# @File  : base.py
# @Author: 叶永彬
# @Date  : 2018/11/15
# @Desc  :
import requests
import inspect
import time,os,json
from common.superAction import SuperAction as SA
from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.path.join(BASE_DIR, ".."))

from Config.Config import Config

from common.logger import logger

from urllib.parse import urljoin


class Req(requests.Session):
    """
    http请求的基础类
    """

    def __init__(self,Session=None):
        super(Req, self).__init__()
        self.conf = Config()
        self.host = self.conf.host
        self.monitor_host = self.conf.monitor_host
        self.zby_host = self.conf.zby_host
        self.aomp_host = self.conf.aomp_host
        self.weiXin_host = self.conf.weiXin_host
        if Session == None:
            self.Session = requests.Session()
        else:
            self.Session = Session

    """pomp"""
    def _api(self,url):
        """host + api_url"""
        full_url = urljoin(self.host,url)
        return full_url

    @property
    def api(self):
        """调用pomp接口地址"""
        return self._api(self.url)

    @property
    def zby_api(self):
        """智泊云调用地址"""
        return self._zby_host(self.url)

    @property
    def monitor_api(self):
        """远程值班调用地址"""
        return self._monitor_host(self.url)

    @property
    def aomp_api(self):
        """aomp调用地址"""
        return self._aomp_host(self.url)

    @property
    def weiXin_api(self):
        """微信商家端调用地址"""
        return self._weiXin_host(self.url)

    def _zby_host(self,url):
        full_url = urljoin(self.zby_host, url)
        return full_url

    def _monitor_host(self,url):
        full_url = urljoin(self.monitor_host, url)
        return full_url

    def _aomp_host(self,url):
        full_url = urljoin(self.aomp_host, url)
        return full_url

    def _weiXin_host(self,url):
        full_url = urljoin(self.weiXin_host, url)
        return full_url

    @property
    def api_headers(self):
        return self.api_headers

    def request(self, method, url, name=None, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method:
            method for the new :class:`Request` object.
        :param url:
            URL for the new :class:`Request` object.
        :param name: (optional)
            Placeholder, make compatible with Locust's HttpSession
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        response = self.Session.request(method, url, **kwargs)
        return response

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        url = self.__formatRule(r'%24%7B(.*?)%7D',url)
        # print(url)
        result = self.request('GET', url, **kwargs)
        self.__getLogFormat(url,kwargs,result)
        return result

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        data = self.__formatCaseParm(data)
        json = self.__formatCaseParm(json)
        result = self.request('POST', url, data=data, json=json, **kwargs)
        self.__postLogFormat(url,data,json,result)
        time.sleep(5)
        tempDataPath.testName = inspect.stack()[2][3]
        return result

    def __formatCaseParm(self,template):
        """
        解析案例保存的储存值
        :return:
        """
        if not template == None:
            template = eval(self.__formatRule(r'\${(.*?)}', str(template)))
            return template
        else:
            return None

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('DELETE', url, **kwargs)

    def __postLogFormat(self,url,data,json,result):
        """
        日志打印格式
        :param url:
        :param data:
        :param json:
        :param result:
        :return:
        """
        logger.info("===请求方式:{}".format('POST'))
        logger.info("===请求路径:{}".format(url))
        if json == None:
            logger.info("===请求参数:{}".format(data))
        else:
            logger.info("===请求参数:{}".format(json))
        logger.info("===返回状态码:{}".format(result.status_code))
        if "mock" in url:
            logger.info("===返回结果:{}".format(SA().changeDate(eval(result.text))))
        else:
            logger.info("===返回结果:{}".format(result.text))


    def __getLogFormat(self,url,kwargs,result):
        """
        get方式的日志打印格式
        :param url:
        :param kwargs:
        :param result:
        :return:
        """
        logger.info("===请求方式:{}".format('GET'))
        logger.info("===请求路径:{}".format(url))
        logger.info("===请求参数:{}".format(kwargs))
        logger.info("===返回状态码:{}".format(result.status_code))
        logger.info("===返回结果:{}".format(result.text))

    def __formatRule(self,rule,template):
        """
        规则模板解析
        rule = r'\${(.*)}'
        rule1 = r'\%24%7B(.*)%7D'
        :return:
        """
        import re
        textList = re.findall(rule, template)
        text_dic = {}
        for key in textList:
            caseName = str(key).split('.')[0]
            keyProperty = str(key).split('.')[1]
            value = self.__get_caseData(keyProperty,caseName)
            text_dic[key] = value
        for key in list(text_dic.keys()):
            strKey = rule.split("(.*?)")[0] + key + rule.split("(.*?)")[1]
            template = re.sub(strKey,text_dic[key],template)
        return template

    def __get_caseData(self,nodeName,caseName = None):
        """
        提取运行案例值
        :return:
        """
        if caseName.lower() == "mytest":
            caseName = str(tempDataPath.runingCaseName).lower() + ".xml"
        else:
            caseName = str(caseName).lower() + ".xml"
        fileList = FloderUtil().getListFloder(root_path + "/temporaryDataLog")
        for file in fileList:
            if self.__getLastFloatName(file).lower() == caseName:
                run_data = XmlHander(file).getValueByName(nodeName)
                return run_data
            else:
                pass

    def __getLastFloatName(self,path):
        """获取最后的文件名"""
        path = str(path).replace("\\","/")
        return path.split('/')[-1]

    def save(self,name,value):
        """
        保存案例中的值
        :return:
        """
        floderPath = tempDataPath.temporaryDataPath
        FloderUtil().createFloder(floderPath)
        filePath = tempDataPath.temporaryDataPath + "/" + tempDataPath.runingCaseName + ".xml"
        XmlHander(filePath).addTag(name, value)

    def getDictBykey(self,json_object,key,expectedValue):
        """
        深度查找json的value值，返回具有value属性的dict
        :param json_object:  传入的json值
        :param key: 属性名
        :param expectedValue: 查找的value值
        :return:
        """
        for k in json_object:
            if k == key:
                if json_object[k] == expectedValue:
                    return json_object
            elif isinstance(json_object[k],list):
                for item in json_object[k]:
                    if isinstance(item,dict):
                        result = self.getDictBykey(item, key, expectedValue)
                        if  result != None:
                            return result
            elif isinstance(json_object[k],dict):
                return self.getDictBykey(json_object[k],key,expectedValue)

    def getDictByList(self,dataList,value,sonValue,expectedValue):
        """
        历遍list列对象，查sonJson的key-value与匹配值返回当前对象
        :param dataList:
        :param expectedValue:
        :return:
        """
        for key in dataList:
            if key[value][sonValue] == expectedValue:
                return key
            else:
                print("return ")

if __name__ == "__main__":
    aa =[{
        'create_time': '2020/03/0312: 06: 09',
        'msg_type': 1,
        'msg_level': 1,
        'content': {
            'inMatch': '1',
            'carSizeTypeInt': 1.0,
            'traderCouponInfoList': [],
            'enterVipName': '临时车',
            'payVal': '5',
            'adjust': False,
            'billCode': '2020030312060790799498',
            'enterTime': '2020/03/0310: 43: 55',
            'abName': '临时车宽出需缴费',
            'parkFee': '5',
            'leaveCarNo': '桂AAAABC4',
            'carSizeType': '小车',
            'carInOutId': '8342',
            'paidVal': '0',
            'normal2Vip': False,
            'favorVal': '0',
            'abType': '9',
            'leaveChannelName': '智泊云接口测试出口',
            'leavePlateImg': 'http: //ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/PLATE/2020030312060536159550-AAAABC4.jpg',
            'leaveChannelId': '2023',
            'stoppingTime': '1小时22分钟10秒',
            'leavePicTime': '2020/03/0312: 06: 05',
            'topBillCode': '200303104352824254241224',
            'leaveCarImg': 'http: //ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/CAR/2020030312060536159550-AAAABC4.jpg'
        },
        'deal_status': 0,
        'id': 28399
    },{
		"id": 28385,
		"content": {
			"favorVal": "0",
			"paidVal": "0",
			"traderCouponInfoList": [],
			"parkFee": "5",
			"leaveCarImg": "http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/CAR/2020030311520272667260-AAAABC4.jpg",
			"normal2Vip": False,
			"abType": "9",
			"billCode": "2020030311520521640065",
			"leaveChannelName": "智泊云接口测试出口",
			"topBillCode": "200303104352824254241224",
			"enterVipName": "临时车",
			"inMatch": "1",
			"leaveChannelId": "2023",
			"stoppingTime": "1小时8分钟7秒",
			"leavePlateImg": "http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/PLATE/2020030311520272667260-AAAABC4.jpg",
			"payVal": "5",
			"carInOutId": "8335",
			"adjust": False,
			"leaveCarNo": "桂AAAABC4",
			"carSizeType": "小车",
			"abName": "临时车宽出需缴费",
			"leavePicTime": "2020/03/03 11:52:02",
			"enterTime": "2020/03/03 10:43:55",
			"carSizeTypeInt": 1.0
		},
		"msg_type": 1,
		"msg_level": 1,
		"create_time": "2020/03/03 11:52:06",
		"deal_status": 0
	},{
		"id": 21111,
		"content": {
			"favorVal": "0",
			"paidVal": "0",
			"traderCouponInfoList": [],
			"parkFee": "5",
			"leaveCarImg": "http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/CAR/2020030311520272667260-AAAABC4.jpg",
			"normal2Vip": False,
			"abType": "9",
			"billCode": "2020030311520521640065",
			"leaveChannelName": "智泊云接口测试出口",
			"topBillCode": "200303104352824254241224",
			"enterVipName": "临时车",
			"inMatch": "1",
			"leaveChannelId": "2023",
			"stoppingTime": "1小时8分钟7秒",
			"leavePlateImg": "http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/03/03/CAR_OUT/2023/PLATE/2020030311520272667260-AAAABC4.jpg",
			"payVal": "5",
			"carInOutId": "8335",
			"adjust": False,
			"leaveCarNo": "桂AAAABC6",
			"carSizeType": "小车",
			"abName": "临时车宽出需缴费",
			"leavePicTime": "2020/03/03 11:52:02",
			"enterTime": "2020/03/03 10:43:55",
			"carSizeTypeInt": 1.0
		},
		"msg_type": 1,
		"msg_level": 1,
		"create_time": "2020/03/03 11:52:06",
		"deal_status": 0
	}]
    # print(aa[1]['content']['enterTime'])
    print(Req().getDictByList(aa,'content','leaveCarNo','桂AAAABC6'))
