# -*- encoding: utf-8 -*-
import psutil
import time
import os
import configparser
from logger import Logger
from utils import get_file_encoding

"""
用于系统进程监控
author: shaipe
create: 2018-11-06
可以使用pyinstaller 将py文件打包为exe文件就可以到其他机器上运行
pyinstaller --onefile --nowindowed --icon=monitor.ico --clean monitor.py
"""


class Monitor:

    def __init__(self):
        self.cpu_count = 0
        self.logger = Logger("monitor", "SysLogs")
        pass

    def get_cpus(self):
        """
        获取cpu数量
        :return:
        """
        if self.cpu_count == 0:
            self.cpu_count = psutil.cpu_count()
            # print(self.cpu_count)
        return self.cpu_count

    def monitor(self, proc_conf):
        """
        开始监控
        :param proc_conf: 监控配置
        :return:
        """

        processs = [p for p in psutil.process_iter(attrs=['pid', 'name', 'username'])
                    if p.info['name'] in proc_conf.keys()]
        # print(processs)
        for proc in processs:
            proc_name = proc.name()
            try:
                # print(proc_name, proc_conf.keys(), proc_name in proc_conf.keys())
                if proc_name in proc_conf.keys():
                    percent = int(proc_conf[proc_name]["percent"])
                    execute = proc_conf[proc_name]["execute"]
                    cpu_percent = proc.cpu_percent(interval=2) / self.get_cpus()
                    # print(":::::", cpu_percent, percent, execute)
                    # 当cpu使用率高于配置的使用率时处理
                    if cpu_percent >= percent:

                        if execute == "":
                            proc.kill()
                        else:
                            if os.path.exists(execute):
                                # print(execute)
                                import subprocess
                                subprocess.call(execute)

                        self.logger.info('Process Name %s, CPU Use Percent %s UserName %s' %
                                         (proc_name, cpu_percent, proc.info["username"]))

                pass
            except psutil.NoSuchProcess:
                pass
        pass

    def get_config(self):
        """
        获取配置信息
        :return:
        """
        try:
            cf = configparser.ConfigParser()
            conf_path = os.path.join(os.getcwd(), 'monitor.ini')
            # print(conf_path)
            if os.path.exists(conf_path):
                encode = get_file_encoding(conf_path)
                cf.read(conf_path, encoding=encode)  # 读取配置文件 encoding用于中文读取
            else:
                with open(conf_path, 'w') as f:
                    f.write("# [config]节点下配置监控时间间隔(秒),interval: 2\n")
                    f.write("# 多节点需添加[process1...]\n# 添加监控进程信息\n#    process: 进程名\n"
                            "#    percent: cpu使用率\n#    execute: cpu问个问题率超过后执行的文件\n\n")
                    cf.add_section("config")
                    cf.set("config", "interval", "2")

                    # 增加section
                    cf.add_section('process1')  # 配合write使用
                    # 修改字段
                    cf.set("process1", "process", "w3wp.exe")
                    cf.set("process1", "percent", "60")
                    cf.set("process1", "execute", "")
                    cf.write(f)

            sections = cf.sections()
            result = dict()
            result["process"] = dict()
            for section in sections:
                if section == "config":
                    result["interval"] = cf.get("config", "interval")
                else:
                    name = cf.get(section, "process").lower()
                    data = {
                        "percent": cf.get(section, "percent"),
                        "execute": cf.get(section, "execute")
                    }
                    result["process"][name] = data
            return result
        except Exception as ex:
            raise ex
            self.logger.error(ex)

    def start(self):
        """
        采用循环的模式间隔5s检测一次
        :return:
        """
        conf = self.get_config()
        # print(conf)
        interval = int(conf.get("interval", 2))

        self.logger.info("Monitor CPU usage Start")

        while True:
            time.sleep(interval)
            self.monitor(conf["process"])
        pass


if __name__ == "__main__":
    Monitor().start()
