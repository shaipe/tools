#!/bin/bash
# 1. vi mongo-install.sh # 创建安装tomcat的安装脚本
# 2. chmod 777 mongo-install.sh # 给定sh的执行权限
# 3. ./mongo-install.sh  # 执行脚本


# 1. 获取安装包
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-amazon2-4.0.2.tgz

# 2. 解压缩
tar zxvf mongodb-linux-x86_64-amazon2-4.0.2.tgz

# 3. 移动文件
mv mongodb-linux-x86_64-amazon2-4.0.2 /usr/local/mongodb

# 4. 进入软件目录
cd /usr/local/mongodb

# 5. 添加环境变量
vi /etc/profile
# export MONGODB_HOME=/usr/local/mongodb
# export PATH=$PATH:$MONGODB_HOME/bin
source /etc/profile

# 6. 查看版本信息
mongo -v

# 7. 启动mongodb, MongoDB需要自建数据库文件夹.
mkdir -p /data/mongodb
mkdir -p /data/mongodb/log
touch /data/mongodb/log/mongodb.log


# 8. 添加配置文件
vi /etc/mongodb.conf
: 'dbpath=/data/mongodb
logpath=/data/mongodb/log/mongodb.log
logappend=true
port=27017
fork=true
##auth = true # 先关闭, 创建好用户在启动'

# 9. 通过配置文件启动
mongod -f /etc/mongodb.conf

# 如果以遇到启动提示GLIBC not found,解决办法如下
:'curl -O http://ftp.gnu.org/gnu/glibc/glibc-2.18.tar.gz
tar zxf glibc-2.18.tar.gz 
cd glibc-2.18/
mkdir build
cd build/
../configure --prefix=/usr
make -j2
make install'
