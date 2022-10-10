import csv
import json
import traceback

import jsonpath
import yaml

from common.logging_util import write_log, error_log
from common.yaml_util import get_object_path


def read_csv_file(csv_path):
    try:
    # 读取csv数据文件
        with open(get_object_path() +"/"+csv_path, encoding='utf-8') as f:
            csv_data_list=[]
            csv_data=csv.reader(f)
            for low in csv_data:
                csv_data_list.append(low)
        return csv_data_list
    except Exception as f:
        error_log("读取报错：异常信息：%s" % str(traceback.format_exc()))
#分析参数化csv
def analysis_parameters(caseinfo):
    try:
        caseinfo_keys = dict(caseinfo).keys()
        if 'parameters' in caseinfo_keys:
            for key, value in dict(caseinfo['parameters']).items():
                caseinfo_str = json.dumps(caseinfo)

                key_list = str(key).split("-")
                lens_flag = True
                csv_data_list = read_csv_file(value)
                one_csv_data = csv_data_list[0]
                for csv_data in csv_data_list:
                    if len(csv_data) != len(one_csv_data):
                        lens_flag = False
                        break
                # 解析
                # 1：规范csv文件书写方式
                new_caseinfo = []
                if lens_flag:
                    for x in range(1, len(csv_data_list)):  # x 行数
                        # tem_caseinfo=json.dumps(caseinfo)
                        temp_caseinfo = caseinfo_str
                        for y in range(0, len(csv_data_list[x])):  # y 列数
                            if csv_data_list[0][y] in key_list:
                                temp_caseinfo = temp_caseinfo.replace("$csv{" + csv_data_list[0][y] + "}",
                                                                      csv_data_list[x][y])
                        new_caseinfo.append(json.loads(temp_caseinfo))
                return new_caseinfo
        else:
            return caseinfo
    except Exception as f:
        error_log("分析参数化报错：异常信息：%s" % str(traceback.format_exc()))


    # 读取yaml测试用例
def read_testcase_file(yaml_path):
    try:
        with open(get_object_path() + yaml_path, encoding='utf-8') as f:
            caseinfo = yaml.load(stream=f, Loader=yaml.FullLoader)
            if len(caseinfo) >=2:
                return caseinfo
            else:
                if jsonpath.jsonpath(*caseinfo,'$.parameters'):
                    new_caseinfo = analysis_parameters(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo
    except Exception as f:
        error_log("读取yaml测试用例报错：异常信息：%s"%str(traceback.format_exc()))


if __name__ == '__main__':
    a=read_testcase_file('/testcases/api/gzh/select_flag.yml')
    print(analysis_parameters(a))