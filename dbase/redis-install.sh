#!/bin/bash
# 1. vi redis-install.sh # 创建安装tomcat的安装脚本
# 2. chmod 777 redis-install.sh # 给定sh的执行权限
# 3. ./redis-install.sh  # 执行脚本

# 1、检查安装依赖程序
yum install gcc-c++
yum install -y ctl

# 2. 获取redis安装文件
curl -O http://download.redis.io/releases/redis-4.0.11.tar.gz

# 3. 解压文件
tar zxvf redis-4.0.11.tar.gz    # 解压缩下载文件

# 4. 移动文件
mv redis-4.0.11 /usr/local/redis    # 移动解压缩文件到指定的目录

# 5. 进入程序目录
cd /usr/local/redis

# 6. 编译安装
make
make install

# 7.  设置配置文件路径
mkdir -p /etc/redis
cp redis.conf /etc/redis

# 8. 修改配置文件
vi /etc/redis/redis.conf # 仅修改： <使用守护进程>daemonize yes （no-->yes） 在vi下可以使用 /daemonize (向下查找) 或 ?daemonize (向上查找)
# 修改bind 服务器ip地址

# 打开防火墙允许其他服务器访问
iptables -I INPUT -p tcp --dport 6379 -j ACCEPT # 配置规则

# 9. 启动
/usr/local/bin/redis-server /etc/redis/redis.conf

# 10. 查看启动
ps -ef| grep redis

# 11. 开机启动配置
echo "/usr/local/bin/redis-server /etc/redis/redis.conf &" >> /etc/rc.local
# 开机启动要配置在 rc.local 中，而 /etc/profile 文件，要有用户登录了，才会被执行。

# 12. 其他配置
redis-cli
# CONFIG set requirepass ""  # 配置访问密码
# AUTH password # 本机访问授权


# 客户端使用
# redis-cli
# redis-cli -h {redis_host} -p {redis_port}
# >set name david
# OK
# >get name
# "david"
# quit
# 关闭客户端
# redis-cli shutdown
