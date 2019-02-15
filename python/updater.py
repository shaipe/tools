# -*- encoding: utf-8 -*-
import os
import os.path
from service_util import WinService, status_code
from zip import ZIP
from logger import Logger
from utils import get_file_md5, post, copytree
from downloader import Downloader


class Updater:

    def __init__(self):
        conf = self.get_config()

        self.domain = conf.get("domain") if hasattr(conf, "domain") else "http://dts.366ec.net"
        self.path = conf.get("path") if hasattr(conf, "path") else "/AutoUpdate.axd"
        self.file_path = os.path.join(os.getcwd(), "Package\\AutoUpdate.zip")
        self.service_name = conf.get("service_name") if hasattr(conf, "service_name") else "AUService"
        pass

    def log(self, txt):
        """
        日志记录
        :param txt: 日志信息
        :return:
        """
        logger = Logger("updater", "SysLogs")
        logger.info(txt)
        pass

    def get_file_encoding(self, file_path, def_encoding='utf-8'):

        """
        获取文件编码方式
        :param file_path: 文件路径
        :param def_encoding: 默认编码方式
        :return:
        """

        import os

        if os.path.exists(file_path):
            with open(file_path, 'rb+') as f:
                import chardet
                encode = chardet.detect(f.read())
                # print(encode)
                enc = encode.get('encoding', def_encoding)
                if enc.lower().startswith('utf-16'):
                    enc = def_encoding

                return enc

        return def_encoding

    def get_config(self):
        """
        获取配置信息
        :return:
        """
        import configparser

        try:
            cf = configparser.ConfigParser()
            conf_path = os.path.join(os.getcwd(), 'updater.ini')
            # print(conf_path)
            if os.path.exists(conf_path):
                encode = self.get_file_encoding(conf_path)
                cf.read(conf_path, encoding=encode)  # 读取配置文件 encoding用于中文读取
            else:
                with open(conf_path, 'w') as f:
                    f.write("# [config] \n# domain: http://dts.366ec.net\n")
                    f.write("# update_path: AutoUpdate.axd\n# service_name: AUService\n")
                    cf.add_section("config")
                    cf.set("config", "domain", "http://dts.366ec.net")
                    cf.set("config", "path", "/AutoUpdate.axd")
                    cf.set("config", "service_name", "AUService")

                    cf.write(f)

            result = dict()
            result["domain"] = cf.get("config", "domain")
            result["path"] = cf.get("config", "path")
            result["service_name"] = cf.get("config", "service_name")
            return result
        except Exception as ex:
            raise ex
            self.logger.error(ex)
        pass

    def is_latest(self):
        """
        判断是否是最新版本
        :return:
        """
        is_last = True
        if os.path.exists(self.file_path):
            fmd5 = get_file_md5(self.file_path)
            rmd5 = post(self.domain + self.path, None, {"action": "packet.md5"})
            if not fmd5.lower() == rmd5.lower():
                is_last = False
        else:
            is_last = False
        return is_last

    def update(self):

        self.log("开始检测服务是否需要更新!")
        try:
            # 判断是否为最新版
            if not self.is_latest():
                self.log("需要更新服务...")
                # 文件如果存在则删除
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                # 下载文件
                url = self.domain + self.path + "?action=FEF96DCFEED03ED8A5D51B0CEBA2956D"
                self.log(f"begin download ... {url}")
                Downloader().download(url, self.file_path)

                self.log("下载完成,解压缩文件...")
                # 下载完后解压文件
                ZIP().unzip_file(self.file_path, os.path.join(os.getcwd(), "Package\\AutoUpdate"), "shaipe")

                win_service = WinService()
                # 停止服务
                self.log("stop service...")
                status = win_service.stop(self.service_name)
                self.log("dsdds" + str(status))
                self.log(f"Service Status: {status_code[status]}...")

                # 复制文件
                self.log("copy files...")
                copytree(os.path.join(os.getcwd(), "Package\\AutoUpdate"), os.getcwd())

                self.log("start Service...")
                # 启动服务
                status = win_service.start(self.service_name)
                self.log(f"update finished, service status: {status_code[status]}!")
            else:
                self.log("已是最新版，不需要更新。")
                win_service = WinService()
                status = win_service.get_service_status(self.service_name)
                self.log(f"current service status: {status_code[status]}!")
                if not status == 4:
                    status = win_service.start(self.service_name)
                    self.log(f"start service of status: {status_code[status]}!")
                pass
            self.log("更新结束!")
        except Exception as ex:
            self.log(f"更新发生异常{ex}")


if __name__ == "__main__":

    # 判断检测是否为最新版本
    Updater().update()
