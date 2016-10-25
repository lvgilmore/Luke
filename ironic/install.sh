#!/usr/bin/env bash

. ./hosts.conf

# install and configure mariadb (mysql)
ssh $ENV_CTRL yum install mariadb mariadb-server python2-PyMySQL
ssh $ENV_CTRL cat >> /etc/my.cnf.d/openstack.cnf << EOF
[mysqld]
bind-address = 10.0.0.11

default-storage-engine = innodb
innodb_file_per_table
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
ssh $ENV_CTRL systemctl enable mariadb.service
ssh $ENV_CTRL systemctl start mariadb.service
scp configs/maria-answers.conf $ENV_CTRL:/tmp
ssh $ENV_CTRL "mysql_secure_installation < /tmp/maria-answers.conf"
