#!/bin/bash
dnf -y remove php
dnf -y install /root/fc38_php8_install_server/remi-release-38-5.fc38.remi.noarch.rpm
dnf --enablerepo=remi -y install php82
dnf --enablerepo=remi -y install php82-php php82-php-xml php82-php-mysqlnd php82-php-opcache php82-php-pgsql php82-php-process php82-php-ldap php82-php-mbstring php82-php-mcrypt php82-php-gd php82-php-bcmath php82-php-pecl-igbinary php82-php-pecl-apcu php82-php-pear php82-php-pecl-memcached php82-php-pecl-memcache
ln -s /usr/bin/php82 /usr/bin/php
cp /etc/opt/remi/php82/php.ini /etc/opt/remi/php82/php.ini.org
cp /mnt/119/3-VDI-CEPH/install/WebItem/php.ini /etc/opt/remi/php82/php.ini
systemctl enable httpd
dnf -y remove firewalld
dnf -y install firewalld
systemctl enable firewalld
systemctl enable cockpit.service
systemctl enable cockpit.socket
reboot
