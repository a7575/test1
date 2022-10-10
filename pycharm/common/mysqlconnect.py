from common.logging_util import LoggerUtil,write_log,error_log
from warnings import filterwarnings
from common.parameters_util import read_testcase_file
import pymysql,pymysql.cursors
from typing import List, Union, Text, Dict
import datetime

filterwarnings("ignore", category=pymysql.Warning)


class mysqldb:
    data = read_testcase_file('config.yml')
    if data['mysql_db']:
        def __init__(self):
            try:
                self.conn = pymysql.connect(
                    host=self.data['host'],
                    user=self.data['user'],
                    password=self.data['password'],
                    port=self.data['port']
                )
                self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            except AttributeError as error:
                LoggerUtil().create_log().error("数据库连接失败,原因：%s", error)

        def __del__(self):
            try:
                self.cur.close()
                self.conn.close()
            except AttributeError as error:
                LoggerUtil().create_log().error("数据库连接失败,原因：%s", error)

        def query(self,sql,state='all'):
            """
                            查询
                            :param sql:
                            :param state:  all 是默认查询全部
                            :return:
                            """
            try:
                self.cur.execute(sql)
                if state=='all':
                    data=self.cur.fetchall()
                else:
                    data=self.cur.fetchone()
                return data
            except AttributeError as error:
                LoggerUtil().create_log().error("数据库连接失败,原因：%s", error)

        def execute(self,sql:Text):
            '''更新。删除，新增
            parama sql'''
            try:
                rows=self.cur.execute(sql)
                self.conn.commit()
                return rows
            except AttributeError as error:
                LoggerUtil().create_log().error("数据库连接失败,原因：%s", error)
                self.conn.rollback()
                raise

        @classmethod
        def sql_data_handler(cls, query_data, data):
            """
            处理部分类型sql查询出来的数据格式
            @param query_data: 查询出来的sql数据
            @param data: 数据池
            @return:
            """
            # 将sql 返回的所有内容全部放入对象中
            for key, value in query_data.items():
                if isinstance(value, dec):
                    data[key] = float(value)
                elif isinstance(value, datetime.datetime):
                    data[key] = str(value)
                else:
                    data[key] = value
            return data

class SetUpMySQL(mysqldb):
    """ 处理前置sql """

    def setup_sql_data(self, sql: Union[List, None]) -> Dict:
        """
            处理前置请求sql
            :param sql:
            :return:
            """
        sql = ast.literal_eval(cache_regular(str(sql)))
        try:
            data = {}
            if sql is not None:
                for i in sql:
                    # 判断断言类型为查询类型的时候，
                    if i[0:6].upper() == 'SELECT':
                        sql_date = self.query(sql=i)[0]
                        for key, value in sql_date.items():
                            data[key] = value
                    else:
                        self.execute(sql=i)
            return data
        except IndexError as exc:
            raise DataAcquisitionFailed("sql 数据查询失败，请检查setup_sql语句是否正确") from exc
