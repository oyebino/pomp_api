# -*- coding: utf-8 -*-
# @File  : base.py
# @Author: 叶永彬
# @Date  : 2018/11/15
# @Desc  :
import requests
import inspect
import time,os,hashlib
from common.superAction import SuperAction as SA
from common.utils import FloderUtil
from common.XmlHander import XmlHander
from Config.parameter import tempDataPath,LoginReponse
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
        self.openYDT_host = self.conf.openYDT_host
        self.mock_host = self.conf.mock_host
        if Session == None:
            self.Session = requests.Session()
        else:
            self.Session = Session

    def __createSigin(self):
        """创建开放平台的sign"""
        m = hashlib.md5()
        m.update(b'test:' + str(tempDataPath.cur_time).encode('utf-8') + b':123456')
        sign = "?sign=" + m.hexdigest()
        return sign

    def __OpenYDT_host(self,url):
        url = url + self.__createSigin()
        full_url = urljoin(self.openYDT_host, url)
        return full_url

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
    def openYDT_api(self):
        """调用pomp接口地址"""
        return self.__OpenYDT_host(self.url)

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

    @property
    def mock_api(self):
        """微信商家端调用地址"""
        return self._mock_host(self.url)

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

    def _mock_host(self,url):
        full_url = urljoin(self.mock_host, url)
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
        if self.__checkLoginStatus(LoginReponse.loginRe):
            kwargs.setdefault('allow_redirects', True)
            url = self.__formatRule(r'%24%7B(.*?)%7D',url)
            result = self.request('GET', url, **kwargs)
            time.sleep(3)
            self.__getLogFormat(url,kwargs,result)
            return result
        else:
            return LoginReponse.loginRe

    def __checkLoginStatus(self,obj):
        """验证登录状态"""
        if not isinstance(obj, dict):
            objDict = obj.json()
        else:
            objDict = obj
        if 'token' not in objDict.keys():
            if 'status' in objDict.keys():
                if objDict['status'] == 2 or objDict['status'] == 400:
                    return False
                else:
                    return True
            if 'state' in objDict.keys():
                if objDict['state'] == True:
                    return True
                else: return False
            if 'error' in objDict.keys():
                if objDict['error'] != 'success':
                    return False
                else:
                    return True
        else:
            return True

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
        if self.__checkLoginStatus(LoginReponse.loginRe):
            data = self.__formatCaseParm(data)
            json = self.__formatCaseParm(json)
            result = self.request('POST', url, data=data, json=json, **kwargs)
            self.__postLogFormat(url,data,json,result)
            time.sleep(3)
            tempDataPath.testName = inspect.stack()[2][3]
            return result
        else:
            return LoginReponse.loginRe

    def __formatCaseParm(self,template):
        """
        解析案例保存的储存值
        :return:
        """
        if not template == None :
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
            if '.' in key:
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

    def getDictBykey(self, json_object,key,expectedValue):
        if isinstance(json_object, list):
            json_object = {'data':json_object}

        return self.getDictBykeySon(json_object,key,expectedValue)


    def getDictBykeySon(self,json_object,key,expectedValue):
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
                result = self.getDictBykey(json_object[k],key,expectedValue)
                if result != None:
                    return result

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

    def setValueByDict(self,json,keyList,value):
        """
        按传进来的keyList，修改key-value值
        :param json:
        :param keyList:
        :param value:
        :return:
        """
        jsonNew = json
        if isinstance(jsonNew, list):
            for j in jsonNew:
                for i in keyList:
                    for key in j.keys():
                        if i == key:
                            if isinstance(j[i], dict):
                                j = j[i]
                            else:
                                j[i] = value
        else:
            for i in keyList:
                for key in jsonNew.keys():
                    if i == key:
                        if isinstance(jsonNew[i], dict):
                            jsonNew = jsonNew[i]
                        else:
                            jsonNew[i] = value
        return json

if __name__ == "__main__":
    a=[{
            'content': {
                'stoppingTime': '15秒',
                'normal2Vip': False,
                'traderCouponInfoList': [],
                'parkFee': '5',
                'enterVipName': '临时车',
                'favorVal': '0',
                'adjust': True,
                'enterTime': '2020/04/07 11:05:48',
                'paidVal': '0',
                'leaveCarImg': 'http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/04/07/CAR_OUT/2064/CAR/2020040711060357713046-BCV906.jpg',
                'abName': '临时车严出需缴费',
                'carInOutId': '12631',
                'leavePlateImg': 'http://ake-parking-test.oss-cn-shenzhen.aliyuncs.com/zbclound-oss/c-i-o-h-s/2KR52FYV/2020/04/07/CAR_OUT/2064/PLATE/2020040711060357713046-BCV906.jpg',
                'carSizeType': '小车',
                'billCode': '2020040711064780847515',
                'carSizeTypeInt': 1.0,
                'leaveCarNo': '粤CCCDB9',
                'leavePicTime': '2020/04/07 11:06:03',
                'topBillCode': '200407110530835739004419',
                'leaveChannelId': '2064',
                'leaveChannelName': '智泊云接口测试出口-严出',
                'abType': '10',
                'inMatch': '1',
                'payVal': '5'
            },
            'deal_status': 0,
            'id': 33096,
            'msg_type': 1,
            'msg_level': 1,
            'create_time': '2020/04/07 11:06:49'
        }]
    try:
        b = Req().getDictByList(a,'content','leaveCarNo','粤CCCDB9')
    except KeyError:
        print('123')