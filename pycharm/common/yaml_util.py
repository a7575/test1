import os

import yaml

#获得项目根目录
def get_object_path():
     return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



#读取extract文件
def read_extract_yaml(node_name):
    with open(get_object_path()+"/extract.yml",encoding='utf-8') as f:
        val = yaml.load(stream=f,Loader=yaml.FullLoader)
        return val[node_name]

#写入extract文件
def write_extract_yaml(data):
    with open(get_object_path()+"/extract.yml",encoding='utf-8',mode='a') as f:
        yaml.dump(data=data,stream=f,allow_unicode=True)

#清空extract文件
def clear_extract_yaml():
    with open(get_object_path()+"/extract.yml",encoding='utf-8',mode='w') as f:
       f.truncate()

#读取config文件
def read_config_yaml(one_node,two_node):
    with open(get_object_path()+"/config.yml",encoding='utf-8') as f:
        val = yaml.load(stream=f,Loader=yaml.FullLoader)
        return val[one_node][two_node]




if __name__ == '__main__':
    print(get_object_path())


