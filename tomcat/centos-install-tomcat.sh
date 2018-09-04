#!/bin/bash
# Apache Tomcat 9.x instructions for installation on CentOS Linux 7

# Apache needs JDK 8 installed on environment (we prefer Oracle JVM HotSpot!)
# find out instructions how to install :D

# A | create tomcat user :: should be run as an unprivileged user
# 1. create a new tomcat group
sudo groupadd tomcat

# 2. create a tomcat user :: 
# member of the tomcat group, home directory of /opt/tomcat (install), shell of /bin/false (nobody login)
sudo useradd -M -s /sbin/nologin -g tomcat -d /opt/tomcat tomcat

# B | installation 
cd ~
mkdir development
wget [http://ftp.unicamp.br/pub/apache/tomcat/tomcat-9/v9.0.0.M22/bin/apache-tomcat-9.0.0.M22.tar.gz]

# install tomcat to the /opt/tomcat directory
sudo mkdir /opt/tomcat
sudo tar xvf apache-tomcat-8*tar.gz -C /opt/tomcat --strip-components=1

# C | update permissions :: proper access to the tomcat installation
cd /opt/tomcat

# tomcat group ownership over the entire installation directory
sudo chgrp -R tomcat /opt/tomcat

# tomcat group read access to the conf directory, and execute access to the directory
sudo chmod -R g+r conf
sudo chmod g+x conf

# make the tomcat user the owner of the directories
sudo chown -R tomcat webapps/ work/ temp/ logs/

# D | install systemd unit file
# create and open unit file service
sudo vim /etc/systemd/system/tomcat.service

# paste the content of tomcat.service [https://gist.github.com/ryanpadilha/a7cb7a31bdbea05fdef3ab3716ca0c9c]

# reload Systemd to load the tomcat unit file
sudo systemctl daemon-reload

# start tomcat service
sudo systemctl start tomcat
sudo systemctl status tomcat

# enable the tomcat service start on server boot (optional)
sudo systemctl enable tomcat
# Created symlink from /etc/systemd/system/multi-user.target.wants/tomcat.service to /etc/systemd/system/tomcat.service.

# change de port of tomcat webserver in conflicts
# search for <Connector port="8080" ...
sudo vim /opt/tomcat/conf/server.xml

# E | tomcat web management interface
# edit tomcat-users.xml file
sudo vim /opt/tomcat/conf/tomcat-users.xml

# add line <user username="admin" password="password" roles="manager-gui,admin-gui"/>
# remove restrict access to the tomcat manager :: comment ip address (loopback)
# 1. manager app
sudo vim /opt/tomcat/webapps/manager/META-INF/context.xml

# 2. host-manager app
sudo vi /opt/tomcat/webapps/host-manager/META-INF/context.xml

# restart the service!
