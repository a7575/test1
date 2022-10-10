# 不可变
# 数字nub 元组tuple 字符串str
#
# 可变
# 字典dict 集合set 列表 list
# import random
#
# print(random.randint(1, 4))
# #字符串
# a='12345'
# print(a[:-2])
# print(a.index('3'))
# b=1
# # a.join()
# a.replace()
# a.index()
# a.split()
# b1=(1,'2',{a:1},(1))
# print(f"{111}b1[2]")
# import os
#
# info1={"name":"修习人生","class":"M211期"}
# a2=[1,2,3]
# a3=1
# add={"xz":18000,"qwxz":25000}
# print(a2.index(2))
# #remove--根据值进行删除 pop---》根据索引删除
# info1.items()
# #取字典的key和value
# #
# # 删除
# a=[1]
# info1.pop("class")
# print(info1)
# print(a.remove(1))
#*kawgs 已元组的方式存储
#**以字典的方式存储
flag=False
def login():
    global flag
    username = input("请输入用户名:")
    password = input("请输入密码:")
    if username == "alex" and password == "123":
        flag = True
        print("登录")
    else:
        flag = False
        print("用户名密码错误")
def wrapper(func):

   def ccc(*ags,**kwags):
       if flag==True:
           ret=func(*ags,*kwags)
           return ret
       else:
           login()

   return ccc
@wrapper
def a():
    pass


a()
# #setup_class 链接数据库，创建日志对象，
# setup 初始化浏览器，读取文件 日志开始
# test
# teardown 关闭浏览器  关闭文件 日志结束
# teardown_class关闭：链接数据库，日志对象，