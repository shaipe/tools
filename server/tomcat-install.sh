#!/bin/bash
# 1. vi tomcat-install.sh # 创建安装tomcat的安装脚本
# 2. chmod 777 tomcat-install.sh # 给定sh的执行权限
# 3. ./tomcat-install.sh  # 执行脚本

# 获取tomcat安装文件
curl -O http://mirror.bit.edu.cn/apache/tomcat/tomcat-9/v9.0.11/bin/apache-tomcat-9.0.11.tar.gz

tar zxvf apache-tomcat-9.0.11.tar.gz    # 解压缩下载文件

mv apache-tomcat-9.0.11 /usr/libexec/tomcat9    # 移动解压缩文件到指定的目录

useradd -M -d /usr/libexec/tomcat9 tomcat   # 添加tomcat用户组

chown -R tomcat. /usr/libexec/tomcat9   # 修改目录操作权限 

vi /usr/lib/systemd/system/tomcat9.service  # 添加Tomcat的服务

systemctl start tomcat9     # 启动tomcat

systemctl enable tomcat9    # 设置tomcat9开机自启动

# 打开8080端口允许网络上的机器访问
# iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8080 -j ACCEPT -m comment --comment "Tomcat Server port"
iptables -I INPUT -p tcp --dport 8080 -j ACCEPT # 配置规则

/usr/sbin/iptables-save  # 保存规则
