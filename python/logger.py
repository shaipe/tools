# -*- coding: utf-8 -*-

import os
import logging
import logging.handlers
import platform
from functools import wraps

if platform.system() == 'Windows':
    from ctypes import windll, c_ulong


    def color_text_decorator(function):
        """
        给文本设置显示颜色
        :param function:
        :return:
        """
        def real_func(self, string):
            windll.Kernel32.GetStdHandle.restype = c_ulong
            h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
            if function.__name__.upper() == 'ERROR':
                windll.Kernel32.SetConsoleTextAttribute(h, 12)
            elif function.__name__.upper() == 'WARN':
                windll.Kernel32.SetConsoleTextAttribute(h, 13)
            elif function.__name__.upper() == 'INFO':
                windll.Kernel32.SetConsoleTextAttribute(h, 14)
            elif function.__name__.upper() == 'DEBUG':
                windll.Kernel32.SetConsoleTextAttribute(h, 15)
            else:
                windll.Kernel32.SetConsoleTextAttribute(h, 15)
            function(self, string)
            windll.Kernel32.SetConsoleTextAttribute(h, 15)

        return real_func
else:
    def color_text_decorator(function):
        """
        给文本设置显示颜色
        :param function:
        :return:
        """
        def real_func(self, string):
            if function.__name__.upper() == 'ERROR':
                self.stream.write('\033[0;31;40m')
            elif function.__name__.upper() == 'WARN':
                self.stream.write('\033[0;35;40m')
            elif function.__name__.upper() == 'INFO':
                self.stream.write('\033[0;33;40m')
            elif function.__name__.upper() == 'DEBUG':
                self.stream.write('\033[0;37;40m')
            else:
                self.stream.write('\033[0;37;40m')
            function(self, string)
            self.stream.write('\033[0m')

        return real_func


class Logger(object):
    """
    日志对象
    """
    DEBUG_MODE = True   # 是否为调试模式

    LOG_LEVEL = 5   # 日志等级

    FORMAT = '%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s'
    # FORMAT = '%(asctime)s %(funcName)s[line:%(lineno)d] %(levelname)s %(message)s'
    # [%(asctime)s] [%(name)s] [%(levelname)s] %(message)s' # 日志输出格式

    ROTATING_MODE = 1   # 日志的切割模式; 1:表示文件大小进行分割,2:表示以时间周期进行分割

    def __init__(self, name, dir_name="logs"):
        """
        构造方法
        :param name:
        """

        self.name = name

        if dir_name is None:
            dir_name = "logs"

        current_path = os.path.join(os.getcwd(), dir_name)
        print(current_path)
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        # base config
        logging.basicConfig()
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG if self.DEBUG_MODE else logging.INFO)
        formatter = logging.Formatter(self.FORMAT)

        if self.ROTATING_MODE == 2:
            # 按时间进行分割处理
            th_all = logging.handlers.TimedRotatingFileHandler(
                os.path.join(current_path, self.name + '_tr.log'), when='midnight', interval=1, backupCount=7)
            th_all.setFormatter(formatter)
            th_all.setLevel(logging.DEBUG)
            self.logger.addHandler(th_all)

        if self.ROTATING_MODE == 1:
            # 按大小进行分割处理
            rh_all = logging.handlers.RotatingFileHandler(
                os.path.join(current_path, self.name + '_fr.log'), mode='a', maxBytes=1024 * 1024 * 2, backupCount=5)
            rh_all.setFormatter(formatter)
            rh_all.setLevel(logging.DEBUG)
            self.logger.addHandler(rh_all)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.DEBUG if self.DEBUG_MODE else logging.INFO)

        self.logger.addHandler(sh)
        self.stream = sh.stream

        # 防止在终端重复打印
        self.logger.propagate = 0

        """
        # output to user define file
        if file_path is None:
            file_path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'logs', 'log1.log')

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            fh = logging.FileHandler()
            fh.setFormatter(formatter)
            fh.setLevel(logging.DEBUG if self.DEBUG_MODE else logging.INFO)

            self.logger.addHandler(fh)
            self.logger.propagate = 0  # 防止重复打印
        """

    @color_text_decorator
    def hint(self, string):
        """
        提示
        :param string:
        :return:
        """
        # 去除多余连续空格
        str_tmp = str(string)
        str_tmp = ' '.join(str_tmp.split())
        if self.LOG_LEVEL >= 5:
            return self.logger.debug(str_tmp)
        else:
            pass

    @color_text_decorator
    def debug(self, string):
        """
        输出调试信息
        :param string:
        :return:
        """
        # 去除多余连续空格
        str_tmp = str(string)
        str_tmp = ' '.join(str_tmp.split())
        if self.LOG_LEVEL >= 4:
            return self.logger.debug(str_tmp)
        else:
            pass

    @color_text_decorator
    def info(self, string):
        """
        直接以信息输出
        :param string:
        :return:
        """
        # 去除多余连续空格
        str_tmp = str(string)
        str_tmp = ' '.join(str_tmp.split())
        if self.LOG_LEVEL >= 3:
            return self.logger.info(str_tmp)
        else:
            pass

    @color_text_decorator
    def warn(self, string):
        """
        输出警告
        :param string:
        :return:
        """
        # 去除多余连续空格
        str_tmp = str(string)
        str_tmp = ' '.join(str_tmp.split())
        if self.LOG_LEVEL >= 2:
            return self.logger.warn(str_tmp)
        else:
            pass

    @color_text_decorator
    def error(self, string):
        """
        错误输出
        :param string:
        :return:
        """
        # print('str:', string)
        # 去除多余连续空格
        str_tmp = str(string)
        str_tmp = ' '.join(str_tmp.split())
        # print(self.LOG_LEVEL, string)
        if self.LOG_LEVEL >= 1:
            return self.logger.error(str_tmp)
        else:
            pass


def log(text, log_type='INFO', name='log', dir_name='logs'):
    """
    记录日志信息
    :param text: 日志文本内容
    :param log_type: 日志类型
    :param name: 日志模块名
    :param dir_name 存放日志的目录
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            logger = Logger(name, dir_name)
            if log_type.upper() == 'ERROR':
                logger.info(text)
            elif log_type.upper() == 'WARN':
                logger.warn(text)
            elif log_type.upper() == 'DEBUG':
                logger.debug(text)
            else:
                logger.info(text)
            return func(*args, **kw)
        return wrapper
    return decorator




