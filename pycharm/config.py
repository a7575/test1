'''web项目地址'''
import os
#根目录
base_url=os.path.dirname(os.path.abspath(__file__))
#用例路径
testcase_dir=os.path.join(base_url,'testcase')
#数据路径
testdatas_dir=os.path.join(base_url,'testdatas')
#测试报告路径
report_dir=os.path.join(base_url,'reports')
#公共日志路径
logs_dir=os.path.join(base_url,'logs/')
#关键字列数
keyword_col=3
#操作值列数
opera_col=6

casesheetsname='用例汇总表'
#汇总表是否执行列数
isexecut_col=5
#汇总表步骤列数
step_col=4
#汇总表测试结果列数
caseresult_col=7
#汇总表执行时间
casetime_col=6

#用例表结果列数
stepresult_col=8
#用例表执行时间
steptime_col=7
os=testdatas_dir+'/testcase.xlsx'


#数据库


if __name__ == '__main__':
    print(os)

# #登录路径
# ogin_url=base_url+'/index/user/login'
# shop_list=base_url+'/shop'
# hop_url=base_url+'/shop/a/23.html'
# #数据
# username="15314408441"
# password="1308694w"
