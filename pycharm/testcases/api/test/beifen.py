
""""""""""""""""""""""""""""""""
#test_01
""""""""""""""""""""""""""""""""



import re

from common.requests_util import RequestUtil
from common.yaml_util import write_extract_yaml, read_extract_yaml


class TestRequests_03:
    def test_php(self):
        url = "/phpwind/"
        res = RequestUtil("base", "base_php_url").send_requests(url=url, method="get")
        return_data = res.text
        #通过正则表达式取值
        obj= re.search('name="csrf_token" value="(.*?)"',return_data)
        #写入extract_token
        extract_data={"csrf_token":obj.group(1)}
        write_extract_yaml(extract_data)



""""""""""""""""""""""""""""""""
#test_02
""""""""""""""""""""""""""""""""

import json
import random

import requests

from common.requests_util import RequestUtil
from common.yaml_util import write_extract_yaml, read_extract_yaml


class TestRequest_03:

    def test_get01(self):

        url = "/cgi-bin/token"
        params = {
                  "grant_type": "client_credential",
                  "appid": "wx5625afce5e19b885",
                  "secret":"c1c4d018981132edc55ed98070c1c0a3"
        }
        res=RequestUtil('base','base_wx_url').send_requests(url=url,method='get',params=params)
        return_data = res.json()
        extract_token={'access_token':return_data['access_token']}
        write_extract_yaml(extract_token)
        print(res.json())

    def test_get02(self):
        url="/cgi-bin/tags/get?access_token"
        params={
            'access_token':read_extract_yaml("access_token")
        }
        res=RequestUtil("base","base_wx_url").send_requests(url=url,method="get",params=params)
        return_data=res.json()
        print(return_data)

    def test_post03(self):
        url="/cgi-bin/tags/create?access_token="+read_extract_yaml("access_token")
        data={"tag":{"name":"ms"+str(random.randint(100000,999999))}}
        res = RequestUtil("base", "base_wx_url").send_requests(url=url, method="post", data=json.dumps(data))
        return_data = res.json()
        print(return_data)

    def test_file_upload(self):
        url="/cgi-bin/media/uploadimg?access_token="+read_extract_yaml("access_token")
        data={
            "media":open(r"E:/1.JPEG","rb")
        }
        res = RequestUtil("base", "base_wx_url").send_requests(url=url, method="post", files=data)
        return_data = res.json()
        print(return_data)


""""""""""""""""""""""""""""""""
#test_03
""""""""""""""""""""""""""""""""
from common.requests_util import RequestUtil
from common.yaml_util import write_extract_yaml, read_extract_yaml


class TestRequest_01:

    def test_01(self):

        url = "/login"
        data = {"username": "admin", "password": "123456"}
        res=RequestUtil('base','base_bd_url').send_requests(url=url,method='post',data=data)
        return_data = res.json()
        extract_token={'Authorization':return_data['data']['token']}
        write_extract_yaml(extract_token)
        print(res.json())

    def test_02(self):
        url = "/menus"
        headers = {
            "Authorization": "{{Authorization}}"
        }
        res = RequestUtil('base', 'base_bd_url').send_requests(url=url, method='get', headers=headers)

        print(res.json())

#8.24 热加载之前

import json
import re

import jsonpath as jsonpath
import requests

from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml


class RequestUtil:

    session = requests.Session()  # 获得session对话对象

    def __init__(self, base, base_url):
        self.base_url = read_config_yaml(base, base_url)
        self.last_headers={}





    # 统一替换val的方法,data可以是url（str），可以是参数（字典，字典中有列表），可以是header（字典）
    def replace_value(self, data):

        if data and isinstance(data, dict):
            str = json.dumps(data)
        else:
            str = data
        for a in range(1, str.count("{{") + 1):
            if "{{" in str and "}}" in str:
                start_index = str.index('{{')
                end_index = str.index("}}")
                old_val = str[start_index:end_index + 2]
                new_val = read_extract_yaml(old_val[2:-2])
                str = str.replace(old_val, new_val)
        if data and isinstance(data, dict):
            data = json.loads(str)
        else:
            data = str
        return data


    def analysis_yaml(self, caseinfo):
        # 必须有四个一级关键字：base_url,name,request,validata
        caseinfo_keys = dict(caseinfo).keys()
        if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys:
              # 二级关键字必须有url，method
              request_keys = dict(caseinfo['request']).keys()
              if 'method' in request_keys and 'url' in request_keys:

                  #参数，请求头，文件上传都不能约束
                  method = caseinfo['request']['method']
                  del caseinfo['request']['method']
                  url = caseinfo['request']['url']
                  del caseinfo['request']['url']
                  headers =None
                  if jsonpath.jsonpath(caseinfo,'$..headers'):
                      headers = caseinfo['request']['headers']
                      del caseinfo['request']['headers']
                  files=None
                  if jsonpath.jsonpath(caseinfo,'$..files'):
                      files=caseinfo['request']['files']
                      for key,value in dict(files).items():
                          files[key]=open(value,"rb")
                      del caseinfo['request']['files']
                  print(caseinfo['request'])
                  res=self.send_requests(method=method, url=url, headers=headers,files=files, **caseinfo['request'])
                  print(res.text)
                  # 提取中间变量
                  return_data = res.json()    #前提是返回json格式，不支持则删除
                  return_text = res.text
                  #
                  # # 正则提取
                  if 'extract' in caseinfo_keys:
                      for key, value in dict(caseinfo['extract']).items():
                          if '(.+?)' in value or '(.*?)' in value:
                              ze_value = re.search(value, return_text)
                              if ze_value:
                                  extract_data = {key: ze_value.group(1)}
                                  write_extract_yaml(extract_data)
                              else:  # josn提取
                                  extract_data = {key: return_data[value]}
                                  write_extract_yaml(extract_data)


              else:

                    print("二级关键字必须有url，method")
        else:
                    print("必须有四个一级关键字：base_url,name,request,validata")

    #统一发送请求
    def send_requests(self, method, url,headers=None,**kwargs):

        # 处理method
        self.last_method = str(method).lower()

        # 处理基础路径
        self.base_url = self.base_url+self.replace_value(url)

        # 处理请求头
        if headers and isinstance(headers, dict):
            self.last_headers = self.replace_value(headers)

        # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
        for key,value in kwargs.items():
            if key in ["params", "data", "json"]:
                kwargs[key] = self.replace_value(value)

        # 发送请求
        res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
                                              **kwargs)
        return res

            # 规范测试用例yaml的写法
import json
import re

import jsonpath as jsonpath
import requests

from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml
from debug_talk import Debug


class RequestUtil:

    session = requests.Session()  # 获得session对话对象

    def __init__(self, base, base_url):
        self.base_url = read_config_yaml(base, base_url)
        self.last_headers={}





    # 统一替换val的方法,data可以是url（str），可以是参数（字典，字典中有列表），可以是header（字典）
#     def replace_value(self, data):
#
#         if data and isinstance(data, dict):
#             str_data = json.dumps(data)
#         else:
#             str_data = data
#         for a in range(1, str_data.count("{{") + 1):
#             if "{{" in str_data and "}}" in str_data:
#                 start_index = str_data.index('{{')
#                 end_index = str_data.index("}}")
#                 old_val = str_data[start_index:end_index + 2]
#                 new_val = read_extract_yaml(old_val[2:-2])
#                 str_data = str_data.replace(old_val, new_val)
#         if data and isinstance(data, dict):
#             data = json.loads(str_data)
#         else:
#             data = str_data
#         return data



 #热加载
    def replace_random(self, data):

        if data and isinstance(data, dict):
            str_data = json.dumps(data)
        else:
            str_data = data
        for a in range(1, str_data.count("${") + 1):
            if "${" in str_data and "}" in str_data:
                #取开始下标
                start_index = str_data.index('${')
                #取结尾下标
                end_index = str_data.index("}")
                #取出来的值
                old_val = str_data[start_index:end_index + 1]
                #对反射中的方法进行解析
                func_name=old_val[2:old_val.index('(')]
                #对反射中的整形进行解析
                args_name=old_val[old_val.index('(')+1:old_val.index(')')]
                #对args-name进行，分割
                a=args_name.split(",")
                #反射，通过反射，在yaml文件中$()调用方法,新的值
                new_val=getattr(Debug(),func_name)(*a)
                str_data = str_data.replace(old_val, str(new_val))
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #规范yaml测试用例写法

    #热加载之后
    def analysis_yaml(self, caseinfo):
        # 必须有四个一级关键字：base_url,name,request,validata
        caseinfo_keys = dict(caseinfo).keys()
        if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys:
              # 二级关键字必须有url，method
              request_keys = dict(caseinfo['request']).keys()
              if 'method' in request_keys and 'url' in request_keys:

                  #参数，请求头，文件上传都不能约束
                  method = caseinfo['request']['method']
                  del caseinfo['request']['method']
                  url = caseinfo['request']['url']
                  del caseinfo['request']['url']
                  headers =None
                  if jsonpath.jsonpath(caseinfo,'$..headers'):
                      headers = caseinfo['request']['headers']
                      del caseinfo['request']['headers']
                  files=None
                  if jsonpath.jsonpath(caseinfo,'$..files'):
                      files=caseinfo['request']['files']
                      for key,value in dict(files).items():
                          files[key]=open(value,"rb")
                      del caseinfo['request']['files']

                  res=self.send_requests(method=method, url=url, headers=headers,files=files, **caseinfo['request'])
                  print(res.text)
                  # 提取中间变量
                  return_data = res.json()    #前提是返回json格式，不支持则删除
                  return_text = res.text
                  #
                  # # 正则提取
                  if 'extract' in caseinfo_keys:
                      for key, value in dict(caseinfo['extract']).items():
                          if '(.+?)' in value or '(.*?)' in value:
                              ze_value = re.search(value, return_text)
                              if ze_value:
                                  extract_data = {key: ze_value.group(1)}
                                  write_extract_yaml(extract_data)
                              else:  # josn提取
                                  extract_data = {key: return_data[value]}
                                  write_extract_yaml(extract_data)
              else:

                    print("二级关键字必须有url，method")
        else:
                    print("必须有四个一级关键字：base_url,name,request,validata")

    #统一发送请求
    def send_requests(self, method, url,headers=None,**kwargs):

        # 处理method
        self.last_method = str(method).lower()

        # 处理基础路径
        self.base_url = self.base_url+self.replace_random(url)
        print(self.base_url)


        # 处理请求头
        if headers and isinstance(headers, dict):
            self.last_headers = self.replace_random(headers)


        # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
        for key,value in kwargs.items():
            if key in ["params", "data", "json"]:

                kwargs[key] = self.replace_random(value)



        # 发送请求
        res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
                                              **kwargs)
        return res



#断言
import json
import re

import jsonpath as jsonpath
import requests

from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml
from debug_talk import Debug


class RequestUtil:

    session = requests.Session()  # 获得session对话对象

    def __init__(self, base, base_url):
        self.base_url = read_config_yaml(base, base_url)
        self.last_headers={}





    # 统一替换val的方法,data可以是url（str），可以是参数（字典，字典中有列表），可以是header（字典）
#     def replace_value(self, data):
#
#         if data and isinstance(data, dict):
#             str_data = json.dumps(data)
#         else:
#             str_data = data
#         for a in range(1, str_data.count("{{") + 1):
#             if "{{" in str_data and "}}" in str_data:
#                 start_index = str_data.index('{{')
#                 end_index = str_data.index("}}")
#                 old_val = str_data[start_index:end_index + 2]
#                 new_val = read_extract_yaml(old_val[2:-2])
#                 str_data = str_data.replace(old_val, new_val)
#         if data and isinstance(data, dict):
#             data = json.loads(str_data)
#         else:
#             data = str_data
#         return data



 #热加载
    def replace_random(self, data):

        if data and isinstance(data, dict):
            str_data = json.dumps(data)
        else:
            str_data = data
        for a in range(1, str_data.count("${") + 1):
            if "${" in str_data and "}" in str_data:
                #取开始下标
                start_index = str_data.index('${')
                #取结尾下标
                end_index = str_data.index("}")
                #取出来的值
                old_val = str_data[start_index:end_index + 1]
                #对反射中的方法进行解析
                func_name=old_val[2:old_val.index('(')]
                #对反射中的整形进行解析
                args_name=old_val[old_val.index('(')+1:old_val.index(')')]
                #对args-name进行，分割
                a=args_name.split(",")
                #反射，通过反射，在yaml文件中$()调用方法,新的值
                new_val=getattr(Debug(),func_name)(*a)
                str_data = str_data.replace(old_val, str(new_val))
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #规范yaml测试用例写法
    def analysis_yaml(self, caseinfo):
        # 必须有四个一级关键字：base_url,name,request,validata
        caseinfo_keys = dict(caseinfo).keys()
        if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys:
              # 二级关键字必须有url，method
              request_keys = dict(caseinfo['request']).keys()
              if 'method' in request_keys and 'url' in request_keys:

                  #参数，请求头，文件上传都不能约束
                  method = caseinfo['request']['method']
                  del caseinfo['request']['method']
                  url = caseinfo['request']['url']
                  del caseinfo['request']['url']
                  headers =None
                  if jsonpath.jsonpath(caseinfo,'$..headers'):
                      headers = caseinfo['request']['headers']
                      del caseinfo['request']['headers']
                  files=None
                  if jsonpath.jsonpath(caseinfo,'$..files'):
                      files=caseinfo['request']['files']
                      for key,value in dict(files).items():
                          files[key]=open(value,"rb")
                      del caseinfo['request']['files']

                  res=self.send_requests(method=method, url=url, headers=headers,files=files, **caseinfo['request'])
                  print(res.text)
                  # 提取中间变量
                  return_data = res.json()    #前提是返回json格式，不支持则删除
                  return_text = res.text
                  status_code=res.status_code
                  #
                  # # 正则提取
                  if 'extract' in caseinfo_keys:
                      for key, value in dict(caseinfo['extract']).items():
                          if '(.+?)' in value or '(.*?)' in value:
                              ze_value = re.search(value, return_text)
                              if ze_value:
                                  extract_data = {key: ze_value.group(1)}
                                  write_extract_yaml(extract_data)
                              else:  # josn提取
                                  extract_data = {key: return_data[value]}
                                  write_extract_yaml(extract_data)
                  #预期结果：caseinfo['validata'],实际结果：return_data，状态码：status_code
                  flag=self.validata_assert(caseinfo['validata'],return_data,status_code)


                  #断言

              else:

                    print("二级关键字必须有url，method")
        else:
                    print("必须有四个一级关键字：base_url,name,request,validata")

    #统一发送请求
    def send_requests(self, method, url,headers=None,**kwargs):

        # 处理method
        self.last_method = str(method).lower()

        # 处理基础路径
        self.base_url = self.base_url+self.replace_random(url)

        # 处理请求头
        if headers and isinstance(headers, dict):
            self.last_headers = self.replace_random(headers)

        # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
        for key,value in kwargs.items():
            if key in ["params", "data", "json"]:

                kwargs[key] = self.replace_random(value)

        # 发送请求
        res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
                                              **kwargs)
        return res


    def validata_assert(self,yq_result,sj_result,status_code):
        # print("""预期结果""")
        # print(yq_result)
        # print("""实际结果""")
        #
        # print(sj_result)

        flag=0
        if yq_result and isinstance(yq_result,list):
            for yq in yq_result:
                for key,value in dict(yq).items():
                    if key=='equals':
                        for assert_key,assert_value in dict(value).items():
                            if assert_key == 'status_code':
                                if status_code!=assert_value:
                                    flag=flag+1
                                    print("断言失败："+assert_key+"不等于"+str(assert_value)+"")
                            else:
                                key_ist= jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
                                if key_ist:
                                    if assert_value not in key_ist:
                                        flag = flag + 1
                                        print("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
                                else:
                                    flag = flag + 1
                                    print("断言失败：返回结果中不存在:"+ assert_key +"")
                    elif key=='contains':
                        if value not in json.dumps(sj_result):
                            flag = flag + 1
                            print("断言失败：返回结果中不包含:" + value + "")
        assert flag==0






""""""""""""""""""""
# import json
# import re
#
# import jsonpath as jsonpath
# import requests
#
# from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml
# from debug_talk import Debug
#
#
# class RequestUtil:
#
#     session = requests.Session()  # 获得session对话对象
#
#     def __init__(self, base, base_url):
#         self.base_url = read_config_yaml(base, base_url)
#         self.last_headers={}
#
#
#
#
#
#     # 统一替换val的方法,data可以是url（str），可以是参数（字典，字典中有列表），可以是header（字典）
# #     def replace_value(self, data):
# #
# #         if data and isinstance(data, dict):
# #             str_data = json.dumps(data)
# #         else:
# #             str_data = data
# #         for a in range(1, str_data.count("{{") + 1):
# #             if "{{" in str_data and "}}" in str_data:
# #                 start_index = str_data.index('{{')
# #                 end_index = str_data.index("}}")
# #                 old_val = str_data[start_index:end_index + 2]
# #                 new_val = read_extract_yaml(old_val[2:-2])
# #                 str_data = str_data.replace(old_val, new_val)
# #         if data and isinstance(data, dict):
# #             data = json.loads(str_data)
# #         else:
# #             data = str_data
# #         return data
#
#
#
#  #热加载
#     def replace_random(self, data):
#
#         if data and isinstance(data, dict):
#             str_data = json.dumps(data)
#         else:
#             str_data = data
#         for a in range(1, str_data.count("${") + 1):
#             if "${" in str_data and "}" in str_data:
#                 #取开始下标
#                 start_index = str_data.index('${')
#                 #取结尾下标
#                 end_index = str_data.index("}")
#                 #取出来的值
#                 old_val = str_data[start_index:end_index + 1]
#                 #对反射中的方法进行解析
#                 func_name=old_val[2:old_val.index('(')]
#                 #对反射中的整形进行解析
#                 args_name=old_val[old_val.index('(')+1:old_val.index(')')]
#                 #对args-name进行，分割
#                 a=args_name.split(",")
#                 #反射，通过反射，在yaml文件中$()调用方法,新的值
#                 new_val=getattr(Debug(),func_name)(*a)
#                 str_data = str_data.replace(old_val, str(new_val))
#         if data and isinstance(data, dict):
#             data = json.loads(str_data)
#         else:
#             data = str_data
#         return data
#
#     #规范yaml测试用例写法
#     def analysis_yaml(self, caseinfo):
#         # 必须有四个一级关键字：base_url,name,request,validata
#         caseinfo_keys = dict(caseinfo).keys()
#         if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys:
#               # 二级关键字必须有url，method
#               request_keys = dict(caseinfo['request']).keys()
#               if 'method' in request_keys and 'url' in request_keys:
#
#                   #参数，请求头，文件上传都不能约束
#                   method = caseinfo['request']['method']
#                   del caseinfo['request']['method']
#                   url = caseinfo['request']['url']
#                   del caseinfo['request']['url']
#                   headers =None
#                   if jsonpath.jsonpath(caseinfo,'$..headers'):
#                       headers = caseinfo['request']['headers']
#                       del caseinfo['request']['headers']
#                   files=None
#                   if jsonpath.jsonpath(caseinfo,'$..files'):
#                       files=caseinfo['request']['files']
#                       for key,value in dict(files).items():
#                           files[key]=open(value,"rb")
#                       del caseinfo['request']['files']
#
#                   res=self.send_requests(method=method, url=url, headers=headers,files=files, **caseinfo['request'])
#                   print(res.text)
#                   # 提取中间变量
#                   return_data = res.json()    #前提是返回json格式，不支持则删除
#                   return_text = res.text
#                   status_code=res.status_code
#                   #
#                   # # 正则提取
#                   if 'extract' in caseinfo_keys:
#                       for key, value in dict(caseinfo['extract']).items():
#                           if '(.+?)' in value or '(.*?)' in value:
#                               ze_value = re.search(value, return_text)
#                               if ze_value:
#                                   extract_data = {key: ze_value.group(1)}
#                                   write_extract_yaml(extract_data)
#                               else:  # josn提取
#                                   extract_data = {key: return_data[value]}
#                                   write_extract_yaml(extract_data)
#                   #预期结果：caseinfo['validata'],实际结果：return_data，状态码：status_code
#                   #flag=self.validata_assert(caseinfo['validata'],return_data,status_code)
#              else:
#
#                     print("二级关键字必须有url，method")
#         else:
#                     print("必须有四个一级关键字：base_url,name,request,validata")
#
#     #统一发送请求
#     def send_requests(self, method, url,headers=None,**kwargs):
#
#         # 处理method
#         self.last_method = str(method).lower()
#
#         # 处理基础路径
#         self.base_url = self.base_url+self.replace_random(url)
#
#         # 处理请求头
#         if headers and isinstance(headers, dict):
#             self.last_headers = self.replace_random(headers)
#
#         # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
#         for key,value in kwargs.items():
#             if key in ["params", "data", "json"]:
#
#                 kwargs[key] = self.replace_random(value)
#
#         # 发送请求
#         res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
#                                               **kwargs)
#         return res
#
# #断言
#     def validata_assert(self,yq_result,sj_result,status_code):
#         # print("""预期结果""")
#         # print(yq_result)
#         # print("""实际结果""")
#         #
#         # print(sj_result)
#
#         flag=0
#         if yq_result and isinstance(yq_result,list):
#             for yq in yq_result:
#                 for key,value in dict(yq).items():
#                     if key=='equals':
#                         for assert_key,assert_value in dict(value).items():
#                             if assert_key == 'status_code':
#                                 if status_code!=assert_value:
#                                     flag=flag+1
#                                     print("断言失败："+assert_key+"不等于"+str(assert_value)+"")
#                             else:
#                                 key_ist= jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
#                                 if key_ist:
#                                     if assert_value not in key_ist:
#                                         flag = flag + 1
#                                         print("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
#                                 else:
#                                     flag = flag + 1
#                                     print("断言失败：返回结果中不存在:"+ assert_key +"")
#                     elif key=='contains':
#                         if value not in json.dumps(sj_result):
#                             flag = flag + 1
#                             print("断言失败：返回结果中不包含:" + value + "")
#         assert flag==0
#





import json
import re

import jsonpath as jsonpath
import requests

from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml
from debug_talk import Debug


class RequestUtil:

    session = requests.Session()  # 获得session对话对象

    def __init__(self, base, base_url):
        self.base_url = read_config_yaml(base, base_url)
        self.last_headers={}





    # 统一替换val的方法,data可以是url（str），可以是参数（字典，字典中有列表），可以是header（字典）
#     def replace_value(self, data):
#
#         if data and isinstance(data, dict):
#             str_data = json.dumps(data)
#         else:
#             str_data = data
#         for a in range(1, str_data.count("{{") + 1):
#             if "{{" in str_data and "}}" in str_data:
#                 start_index = str_data.index('{{')
#                 end_index = str_data.index("}}")
#                 old_val = str_data[start_index:end_index + 2]
#                 new_val = read_extract_yaml(old_val[2:-2])
#                 str_data = str_data.replace(old_val, new_val)
#         if data and isinstance(data, dict):
#             data = json.loads(str_data)
#         else:
#             data = str_data
#         return data



 #热加载
    def replace_random(self, data):

        if data and isinstance(data, dict):
            str_data = json.dumps(data)
        else:
            str_data = data
        for a in range(1, str_data.count("${") + 1):
            if "${" in str_data and "}" in str_data:
                #取开始下标
                start_index = str_data.index('${')
                #取结尾下标
                end_index = str_data.index("}")
                #取出来的值
                old_val = str_data[start_index:end_index + 1]
                #对反射中的方法进行解析
                func_name=old_val[2:old_val.index('(')]
                #对反射中的整形进行解析
                args_name=old_val[old_val.index('(')+1:old_val.index(')')]
                #对args-name进行，分割
                a=args_name.split(",")
                #反射，通过反射，在yaml文件中$()调用方法,新的值
                new_val=getattr(Debug(),func_name)(*a)
                str_data = str_data.replace(old_val, str(new_val))
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #规范yaml测试用例写法
    def analysis_yaml(self, caseinfo):
        # 必须有四个一级关键字：base_url,name,request,validata
        caseinfo_keys = dict(caseinfo).keys()
        if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys:
            # 二级关键字必须有url，method
            request_keys = dict(caseinfo['request']).keys()
            if 'method' in request_keys and 'url' in request_keys:

                  #参数，请求头，文件上传都不能约束
                  method = caseinfo['request']['method']
                  del caseinfo['request']['method']
                  url = caseinfo['request']['url']
                  del caseinfo['request']['url']
                  headers =None
                  if jsonpath.jsonpath(caseinfo,'$..headers'):
                      headers = caseinfo['request']['headers']
                      del caseinfo['request']['headers']
                  files=None
                  if jsonpath.jsonpath(caseinfo,'$..files'):
                      files=caseinfo['request']['files']
                      for key,value in dict(files).items():
                          files[key]=open(value,"rb")
                      del caseinfo['request']['files']

                  res=self.send_requests(method=method, url=url, headers=headers,files=files, **caseinfo['request'])
                  print(res.text)
                  # 提取中间变量
                  return_data = res.json()    #前提是返回json格式，不支持则删除
                  return_text = res.text
                  status_code=res.status_code
                  # 预期结果：caseinfo['validata'],实际结果：return_data，状态码：status_code

                  #
                  # # 正则提取
                  if 'extract' in caseinfo_keys:
                      for key, value in dict(caseinfo['extract']).items():
                          if '(.+?)' in value or '(.*?)' in value:
                              ze_value = re.search(value, return_text)
                              if ze_value:
                                  extract_data = {key: ze_value.group(1)}
                                  write_extract_yaml(extract_data)
                          else:
                              # josn提取
                              extract_data = {key: return_data[value]}
                              write_extract_yaml(extract_data)

                  self.validata_assert(caseinfo['validata'], return_data, status_code)

            else:

                    print("二级关键字必须有url，method")

                    print("必须有四个一级关键字：base_url,name,request,validata")

    #统一发送请求
    def send_requests(self, method, url,headers=None,**kwargs):

        # 处理method
        self.last_method = str(method).lower()

        # 处理基础路径
        self.base_url = self.base_url+self.replace_random(url)

        # 处理请求头
        if headers and isinstance(headers, dict):
            self.last_headers = self.replace_random(headers)

        # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
        for key,value in kwargs.items():
            if key in ["params", "data", "json"]:

                kwargs[key] = self.replace_random(value)

        # 发送请求
        res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
                                              **kwargs)
        return res

#断言
    def validata_assert(self,yq_result,sj_result,status_code):
        # print("""预期结果""")
        # print(yq_result)
        # print("""实际结果""")
        #
        # print(sj_result)

        flag=0
        if yq_result and isinstance(yq_result,list):
            for yq in yq_result:
                for key,value in dict(yq).items():
                    if key=='equals':
                        for assert_key,assert_value in dict(value).items():
                            if assert_key == 'status_code':
                                if status_code!=assert_value:
                                    flag=flag+1
                                    print("断言失败："+assert_key+"不等于"+str(assert_value)+"")
                            else:
                                key_ist= jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
                                if key_ist:
                                    if assert_value not in key_ist:
                                        flag = flag + 1
                                        print("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
                                else:
                                    flag = flag + 1
                                    print("断言失败：返回结果中不存在:"+ assert_key +"")
                    elif key=='contains':
                        if value not in json.dumps(sj_result):
                            flag = flag + 1
                            print("断言失败：返回结果中不包含:" + value + "")
        assert flag==0




















