import base64
import hashlib
import random

import rsa

from common.yaml_util import read_extract_yaml, read_config_yaml


class Debug:
    # 获得随机数
    def get_random(self, min, max):
        return random.randint(int(min), int(max))

    # 获得extract。yml中的值
    def get_extract_data(self, node_name):
        return read_extract_yaml(node_name)

    def get_base_url(self, node_name):
        return read_config_yaml('base', node_name)


    def get_sql(self,a='tags'):
        return  a

        # MD5加密
    def md5(self, args=None):
        if args is None:
            # utf8_str = str(args).encode("utf-8")
            # # md5加密（哈希算法）
            # md5_str = hashlib.md5(utf8_str).hexdigest()
            md5_str = ''
            return md5_str  # 返回为小写，需要转大写后面添加.upper
        else:
            utf8_str = str(args).encode("utf-8")
            # md5加密（哈希算法）
            md5_str = hashlib.md5(utf8_str).hexdigest()
            return md5_str  # 返回为小写，需要转大写后面添加.upper

        # BASE64加密

    def bs64(self, args):
        # 以指定的编码格式编码字符串
        utf8_str = str(args).encode("utf-8")
        # base64加密
        base64_str = base64.b64encode(utf8_str).decode("utf-8")  # base64.b64encode(utf8_str)是字节格式，使用decode(
        # "utf-8")将其转换成字符串
        return base64_str  # 返回为小写，需要转大写后面添加.upper

    # RSA双密钥加密方式
    # 生成公钥的私钥写入到指定的pem文件：
    def create_key(self):
        # 根据密钥长度生成公钥和私钥
        (public_key, private_key) = rsa.newkeys(1024)
        # print(public_key,private_key)
        # 保存公钥
        with open("C:pycharm\\public.pem", "w+") as f:
            f.write(public_key.save_pkcs1().decode())
        # 保存私钥
        with open("C:pycharm\\private.pem", "w+") as f:
            f.write(private_key.save_pkcs1().decode())

    # 通过公钥加密
    def public_key_jiami(self, args):
        # 导入密钥
        with open("public.pem") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
        # 加密
        byte_str = rsa.encrypt(str(args).encode("utf-8"), pubkey)
        print(byte_str)
        # 把二进制转换成字符串格式
        miwen = base64.b64encode(byte_str).decode('utf-8')
        return miwen

    # 通过私钥解密
    def private_key_jiemi(self, args):
        # 导入私钥
        with open("private.pem") as f:
            prikey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        # 解密
        byte_str = base64.b64decode(args)
        mingwen = rsa.decrypt(byte_str, prikey).decode()
        return mingwen

    # # 签名
    # def signs(self,yaml_name):
    #     last_url=""
    #     last_data= {}
    #     with open(os.getcwd() + yaml_name, mode='r', encoding='utf-8') as f:
    #         yaml_value = yaml.load(f, yaml.FullLoader)
    #         for  caseinfo in yaml_value:
    #             caseinfo_keys=caseinfo.keys()
    #             #判断一级关键字是否包括有：name,request,valiedate
    #             if "request" in caseinfo_keys:
    #                 # 判断url
    #                 if "url" in caseinfo['request'].keys():
    #                     last_url=caseinfo['request']['url']
    #                 #判断参数
    #                 req=caseinfo['request']
    #                 for key,value in req.items():
    #                     if key in ['params','data','json']:
    #                         for p_key,p_value in req[key].items():
    #                             last_data[p_key]=p_value
    #     last_url=last_url[last_url.index("?")+1:len(last_url)]
    #     #把last_url的字符串格式加到last_data改成字典
    #     lis=last_url.split("&")
    #     for a in lis:
    #         last_data[ a[0:a.index("=")]]=a[a.index("="):len(a)]
    #     #热加载替换
    #     last_url=RequestUtil(self).replace_value(last_url)
    #     last_data=RequestUtil(self).replace_value(last_data)
    #     #字典根据key的asscii码排序
    #     new_dict=self.dict_asscii_sort(last_data)
    #     #第二步,把参数名和参数值用=连接成字符串，多个参数直接用&连接
    #     new_str=""
    #     for key,value in new_dict.items():
    #         new_str=new_str+key+"="+value+"&"
    #     #第三步到第五步
    #     appid=""
    #     appsecret=""
    #     nonce=str(random.randint(1000000000,9999999999))
    #     timestamp=str(time.time())
    #     all_str=appid+appsecret+new_str+nonce+timestamp
    #     #第六步
    #     sign_str=self.md5(all_str).upper()
    #     return sign_str
    #
    # def dict_asscii_sort(self,dict_str):
    #     dict_key=dict(dict_str).keys()
    #     l=list(dict_key)
    #     l.sort()
    #     new_dict={}
    #     for key in l:
    #         new_dict[key]=dict_str[key]
    #     return new_dict
