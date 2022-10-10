import logging
import config as cf
import time
import os
from common.yaml_util import get_object_path, read_config_yaml


class LoggerUtil:
     def create_log(self,logger_name='log'):
         #创建一个日志对象
         self.logger=logging.Logger(logger_name)
         #设置全局日志级别
         self.logger.setLevel(logging.DEBUG)
         if not self.logger.handlers:
             # coding=utf-8--------文件日志--------------------------
             #获得文件日志的路径
             self.log_file_path=os.path.join(cf.logs_dir, f"log_{time.strftime('%Y%m%d%H%M%S', time.localtime())}")+".log"
             #创建文件日志控制器
             self.file_header=logging.FileHandler(self.log_file_path,encoding='utf-8')
             #文件日志级别
             logger_file_level=str(read_config_yaml('log', 'log_level')).lower()
             if logger_file_level == 'debug':
                 self.file_header.setLevel(logging.DEBUG)
             if logger_file_level == 'info':
                 self.file_header.setLevel(logging.INFO)
             if logger_file_level == 'warning':
                 self.file_header.setLevel(logging.WARNING)
             if logger_file_level == 'error':
                 self.file_header.setLevel(logging.ERROR)
             if logger_file_level == 'critical':
                 self.file_header.setLevel(logging.CRITICAL)
             # 创建文件日志格式
             self.file_header.setFormatter(logging.Formatter(read_config_yaml('log','log_formate')))
             #控制器加入日志对象
             self.logger.addHandler(self.file_header)
             #--------控制台日志-----------------------------

             # 创建控制台日志控制器
             self.console_header = logging.StreamHandler()
             # 控制台日志级别
             logger_console_level = str(read_config_yaml('log', 'log_level')).lower()
             if logger_console_level == 'debug':
                 self.console_header.setLevel(logging.DEBUG)
             if logger_console_level == 'info':
                 self.console_header.setLevel(logging.INFO)
             if logger_console_level == 'warning':
                 self.console_header.setLevel(logging.WARNING)
             if logger_console_level == 'error':
                 self.console_header.setLevel(logging.ERROR)
             if logger_console_level == 'critical':
                 self.console_header.setLevel(logging.CRITICAL)
             # 创建控制台件日志格式
             self.console_header.setFormatter(logging.Formatter(read_config_yaml('log', 'log_formate')))
             # 控制器加入日志对象
             self.logger.addHandler(self.console_header)
         return self.logger

#输出日志
def write_log(log_message):
    LoggerUtil().create_log().info(log_message)

#抛出异常日志
def error_log(log_message):
    LoggerUtil().create_log().error(log_message)
    raise Exception(log_message)





if __name__ == '__main__':
     print(LoggerUtil().create_log().info('test'))





