
## 工程目录：

- Project/:  系统名称
  - interface   接口基础类
  - Api  接口基础类封装
  - common  公共方法类(日志,数据库等)
  - Config 配置文件
  - lib 依赖插件库
  - report/： 存储测试结果
  - result  存放运行截图
  - Log  执行日志
  - test_data 业务数据
  - test_suit 接口测试用例集
  - run_test:  执行接口测试入口

## 说明
**1.Api文件夹存放各模块业务接口的封装**

**2.test_data 存放用例业务数据，以便维护**

- 格式为yml管理,场景测试用例业务结构如下：
```
- test:
    name: 收费放行
    desc: 验证正常收费放行
    send_data:
      channel_in: {lightRule_inChannelCode}
      clientId_in: {lightRule_inClientID}
      channel_out: {lightRule_outChannelCode}
      clientId_out: {lightRule_outClientID}
      leaveType: 2
    except:
      status_code: 200

- test:
    name: 异常放行
    desc: 验证异常收费放行
    send_data:
      channel_in: {lightRule_inChannelCode}
      clientId_in: {lightRule_inClientID}
      channel_out: {lightRule_outChannelCode}
      clientId_out: {lightRule_outClientID}
      leaveType: 3
    except:
      status_code: 200
```
- 在yml中,使用中括号加参数能直接配置文件里的值，如：
```
{lightRule_inChannelCode}
{lightRule_parkID}
```

**3.test_suit文件保存按模块的执行用例，用例文件及用例方法必须以test为前缀**

```
def test_CarIn(self):
	pass
```

**4.report存放测试报告**

**5.run_test 批量执行测试案例的触发文件；**

**6.web-report.bat 该文件是自动生成报告显示,通过run_test文件执行后，双击执行能正常显示报告**

## 使用方法：

- 安装python3环境(未在python2上运行过，不知道有没有问题）
- clone代码到本地
- cmd到根目录下载相关依赖包

```
pip install -r requirements.txt
```
- 配置allure报告插件

  - 解压allure压缩包

    ```
    lib\allure-2.7.0.zip
    ```

  - 配置环境变量 
  ```
  path = E:\allure-2.7.0\bin;
  ```
