#!/bin/bash
dnf -y install net-snmp
mkdir -p /var/www/file/snmp
chown -R apache:apache /var/www/file
snmptranslate -m +ACRORED-MIB -IR -On acrored
export MIBS=+ALL
pip install pysnmp
pip install pysmi
dnf -y install mariadb-connector-c mariadb-connector-c-devel
pip install mariadb
mkdir -p /root/art/snmp
mkdir -p /root/art/snmp/utils
mkdir -p /root/art/snmp/config
reboot
