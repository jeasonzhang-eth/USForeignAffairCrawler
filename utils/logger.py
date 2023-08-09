# -*- encoding: utf-8 -*-
"""
@File    :   logger.py.py   
@Contact :   zhangjie2@cuhk.edu.cn
@License :   (C)Copyright 2018-2023
 
@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2023/8/8 14:05   JeasonZhang      1.0         None
"""
from utils.tools import singleton_class_decorator

"""
 日志封装类，导入即可直接使用
# 当前文件名 logger.py
"""

import os
import datetime
import loguru


@singleton_class_decorator
class Logger:
    def __init__(self):
        self.logger_add()

    @staticmethod
    def get_project_path(project_path=None):
        if project_path is None:
            # 当前项目文件的，绝对真实路径
            # 路径，一个点代表当前目录，两个点代表当前目录的上级目录
            project_path = os.path.realpath('../src/utils')
        # 返回当前项目路径
        return project_path

    def get_log_path(self):
        # 项目目录
        project_path = self.get_project_path()
        # 项目日志目录
        project_log_dir = os.path.join(project_path, '../src/utils/logs')
        # 日志文件名
        project_log_filename = 'runtime_{}.log'.format(datetime.date.today())
        # 日志文件路径
        project_log_path = os.path.join(project_log_dir, project_log_filename)
        # 返回日志路径
        return project_log_path

    def logger_add(self):
        loguru.logger.add(
            # 水槽，分流器，可以用来输入路径
            sink=self.get_log_path(),
            # 日志创建周期,这里也可以配置成文件大小，例如10 MB
            rotation='00:00',
            # 保存
            retention='1 year',
            # 文件的压缩格式
            compression='zip',
            # 编码格式
            encoding="utf-8",
            # 具有使日志记录调用非阻塞的优点
            enqueue=True,
            # 配置日志等级，配置这里是只保存有用信息到文件，debug信息剔除
            level='INFO'
        )

    @property
    def get_logger(self):
        return loguru.logger


if __name__ == '__main__':
    """
    在其他.py文件中，只需要直接导入已经实例化的logger类即可，会将日志文件按照日期保存到logs目录下
    例如从lib文件夹内导入如下：
    from lib.logger import Logger
    然后直接使用
     logger = Logger().get_logger
     logger.级别（输出内容即可）
    """
    logger = Logger().get_logger
    logger.debug('调试代码')
    logger.info('输出信息')
    logger.success('输出成功')
    logger.warning('错误警告')
    logger.error('代码错误')
    logger.critical('崩溃输出')
