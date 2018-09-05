# centos 安装以及初始配置

## 1. 安装成功后配置网络

```shell
# centos 默认安装成功后网络是关闭状态
# centos启动好以后,修改配置文件
cd /etc/sysconfig/network-scripts/
# 一般情况下网卡的配置信息存储在: ifcfg-eth0中
vi ifcfg-eth0
# 修改ONBOOT=no 为 ONBOOT=yes 
service network restart # 然后重启网络服务
```