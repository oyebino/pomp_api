
## 工程目录：

- Project/:  系统名称
  - Api  模块接口基础类封装
  - common  公共方法类(日志,数据库等)
  - Config 配置文件
  - lib 依赖插件库
  - report/： 存储测试结果
  - result  存放运行截图
  - temporaryDataLog 案例临时数据
  - Log  执行日志
  - test_data 用例业务数据
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
      channel_in: ${lightRule_inChannelCode}
      clientId_in: ${lightRule_inClientID}
      channel_out: ${lightRule_outChannelCode}
      clientId_out: ${lightRule_outClientID}
      leaveType: 2
    except:
      status_code: 200

- test:
    name: 异常放行
    desc: 验证异常收费放行
    send_data:
      channel_in: ${lightRule_inChannelCode}
      clientId_in: ${lightRule_inClientID}
      channel_out: ${lightRule_outChannelCode}
      clientId_out: ${lightRule_outClientID}
      leaveType: 3
    except:
      status_code: 200
```
- 在yml中,使用"${}"加参数能直接配置文件里的值，如：
```
${lightRule_inChannelCode}
${lightRule_parkID}
```
- 在yml中，引用superAction类文件的方法(必须要有返回值)，可直接在配置文件的值，如：
```
${__create_carNum()}
${__create_carNum(1,2)}
${__create_carNum(carType="民航")}
${__create_carNum(3,5,carType="民航")}
```
- 在用例文件执行过程中能保存案例运行值，以xml文件形式保存在temporaryDataLog文件夹内，案例文件类需要继承baseCase基类，self.save_data("字段名","值")
```
class TestCarStrictRuleInOutNoPay(BaseCase):

	self.save_data('carIn_jobId',result['biz_content']['job_id'])

```
- 在用例数据yml中，提取保存的值，${用例名.变量},如引用当前案例储存的值可${mytest.变量}
```
- test:
    name: 异常放行
    desc: 验证异常收费放行
    send_data:
      carNo: ${异常放行.carNum}
      leaveType: 3
    except:
      status_code: 200
```
- 在用例数据yml中，可以运行基本的运行代码块，用"{{}}"表示(需要添加双引用)，如
```
- test:
    name: 异常放行
    desc: 验证异常收费放行
    send_data:
      carNo: ${异常放行.carNum}
      leaveType: 3
    except:
      num: "{{1+1}}"
```

**3.test_suit文件保存按模块的执行用例，用例文件，类名及用例方法必须以test为前缀**

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
