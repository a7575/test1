import json
import re
import traceback

import jsonpath as jsonpath
import requests

from common.logging_util import write_log, error_log
from common.yaml_util import read_config_yaml, read_extract_yaml, write_extract_yaml
from debug_talk import Debug


class RequestUtil:
    session = requests.Session()  # 获得session对话对象

    def __init__(self, ):
        self.base_url = ""
        self.last_headers = {}

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

    # 热加载
    def replace_random(self, data):
        if data and isinstance(data, dict):
            str_data = json.dumps(data)
        else:
            str_data = data
        for a in range(1, str_data.count("${") + 1):
            if "${" in str_data and "}" in str_data:
                # 取开始下标
                start_index = str_data.index('${')
                # 取结尾下标
                end_index = str_data.index("}")
                # 取出来的值
                old_val = str_data[start_index:end_index + 1]
                # 对反射中的方法进行解析
                func_name = old_val[2:old_val.index('(')]
                # 对反射中的整形进行解析
                args_name = old_val[old_val.index('(') + 1:old_val.index(')')]
                # 对args-name进行，分割
                a = args_name.split(",")
                # 反射，通过反射，在yaml文件中$()调用方法,新的值
                new_val = getattr(Debug(), func_name)(*a)
                str_data = str_data.replace(old_val, str(new_val))
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    # 规范yaml测试用例写法
    def analysis_yaml(self, caseinfo):
        try:
            # 必须有四个一级关键字：base_url,name,request,validata
            caseinfo_keys = dict(caseinfo).keys()
            if 'name' in caseinfo_keys and 'base_url' in caseinfo_keys and 'request' in caseinfo_keys and 'validata' in caseinfo_keys :
                self.base_url=caseinfo['base_url']
                # requests下二级关键字必须有url，method
                request_keys = dict(caseinfo['request']).keys()
                if 'method' in request_keys and 'url' in request_keys:
                    self.name = caseinfo['base_url']
                    name = caseinfo['name']
                    # 参数，请求头，文件上传都不能约束
                    method = caseinfo['request']['method']
                    del caseinfo['request']['method']
                    url = caseinfo['request']['url']
                    del caseinfo['request']['url']
                    headers = None
                    if jsonpath.jsonpath(caseinfo, '$..headers'):
                        headers = caseinfo['request']['headers']
                        del caseinfo['request']['headers']
                    files = None
                    if jsonpath.jsonpath(caseinfo, '$..files'):
                        files = caseinfo['request']['files']
                        for key, value in dict(files).items():
                            files[key] = open(value, "rb")
                        del caseinfo['request']['files']
                    # 收集日志
                    write_log("----------接口请求开始-------------")
                    res = self.send_requests(name=name,method=method, url=url, headers=headers, files=files,
                                             **caseinfo['request'])

                    return_data = res.json()  # 前提是返回json格式，不支持则删除
                    return_text = res.text
                    status_code = res.status_code
                    # 预期结果：caseinfo['validata'],实际结果：return_data，状态码：status_code
                    # # # 提取中间变量
                    if 'extract' in caseinfo_keys:
                         for key, value in dict(caseinfo['extract']).items():
                            # ,正则提取
                            if '(.+?)' in value or '(.*?)' in value:
                                ze_value = re.search(value, return_text)
                                if ze_value:
                                    extract_data = {key: ze_value.group(1)}
                                    write_extract_yaml(extract_data)
                            else:
                                # josn提取
                                extract_data = {key: return_data[value]}
                                write_extract_yaml(extract_data)
                    # 断言的封装
                    yq_result = caseinfo['validata']
                    self.validata_assert(caseinfo['validata'], return_data, status_code)
                else:
                    error_log("二级关键字必须有url，method")
            else:
                error_log("必须有四个一级关键字：base_url,name,request,validata")
        except Exception as f:
            error_log("热加载报错：异常信息：%s" % str(traceback.format_exc()))

    # 统一发送请求
    def send_requests(self,name, method, url,file=None, headers=None, **kwargs):
        try:
            # 处理method
            self.last_method = str(method).lower()
            # 处理基础路径
            self.base_url = self.replace_random(self.base_url) + self.replace_random(url)
            # 处理请求头
            if headers and isinstance(headers, dict):
                self.last_headers = self.replace_random(headers)

            # 处理请求数据，请求数据可以是params，json，data，那对kwargs做解析
            for key, value in kwargs.items():
                if key in ["params", "data", "json"]:
                    kwargs[key] = self.replace_random(value)
            # 收集日志
            write_log('接口名称：%s'%name)
            write_log('请求方发：%s'%self.last_method)
            write_log('请求路径：%s'%self.base_url)
            if 'params' in kwargs.keys():
                write_log('请求参数：%s'%kwargs['params'])
            elif 'json' in kwargs.keys():
                write_log('请求参数：%s'%kwargs['json'])
            elif 'data' in kwargs.keys():
                write_log('请求参数：%s'%kwargs['data'])
            write_log('文件上传：%s'%file)
            write_log('请求头：%s'%self.last_headers)
            # 发送请求
            res = RequestUtil.session.request(method=self.last_method, url=self.base_url, headers=self.last_headers,
                                              **kwargs)
            return res
        except Exception as f:
            error_log("统一发送请求报错：异常信息：%s" % str(traceback.format_exc()))

    # 断言
    def validata_assert(self, yq_result, sj_result, status_code):
        try:

            # print("""预期结果""")
            # print(yq_result)
            # print("""实际结果""")
            #
            # print(sj_result)
            #收集日志
            write_log('预期结果：%s'%yq_result)
            write_log('实际结果：%s'%sj_result)
            flag = 0
            if yq_result and isinstance(yq_result, list):
                for yq in yq_result:
                    for key, value in dict(yq).items():
                        if key == 'equals':
                            for assert_key, assert_value in dict(value).items():
                                if assert_key == 'status_code':
                                    if status_code != assert_value:
                                        flag = flag + 1
                                        error_log("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
                                else:
                                    key_ist = jsonpath.jsonpath(sj_result, '$..%s' % assert_key)
                                    if key_ist:
                                        if assert_value not in key_ist:
                                            flag = flag + 1
                                            error_log("断言失败：" + assert_key + "不等于" + str(assert_value) + "")
                                    else:
                                        flag = flag + 1
                                        error_log("断言失败：返回结果中不存在:" + assert_key + "")
                        elif key == 'contains':
                            if value not in json.dumps(sj_result):
                                flag = flag + 1
                                error_log("断言失败：返回结果中不包含:" + value + "")

                        elif key == 'sql':
                            if value not in json.dumps(sj_result):
                                flag = flag + 1
                                error_log("断言失败：返回结果中不包含:" + value + "")
                        else:
                            print("框架不支持此断言方式")
            assert flag == 0
            write_log("----------接口请求成功-------------")
            write_log("----------接口请求结束-------------")
        except Exception as f:
            error_log("断言报错：异常信息：%s" % str(traceback.format_exc()))
