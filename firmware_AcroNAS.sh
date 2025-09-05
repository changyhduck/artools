#!/bin/sh

mkdir /mnt/119
mount1; mount -t cifs //192.168.88.119/thttpd  /mnt/119 -o username=thttpd,password=thttpd


mkdir -p /var/www/html/script
mkdir /var/www/html/updateFilePath
mkdir /var/www/html/check_update
mkdir /mnt/tmpfs
mkdir -p /root/art/script

cd /root
mkdir /storage
mkdir /artgluster

cp -f /mnt/119/5-AcroStor-Fedora/install/script/*.sh /var/www/html/script/
cp -f /mnt/119/5-AcroStor-Fedora/install/script/*.py /var/www/html/script/

# ********************************************************
# . /mnt/119/5-AcroStor-Fedora/install/install_web.sh 1  --->
# ********************************************************
mkdir -p /LocalDB/admin/session
mkdir -p /LocalDB/manager/session
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/config.pwd /LocalDB/config.pwd
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/pwd /LocalDB/admin/pwd
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/slat /LocalDB/admin/slat
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/pwd /LocalDB/manager/pwd
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/slat /LocalDB/manager/slat
chown -R apache:apache /LocalDB


cp /mnt/119/5-AcroStor-Fedora/install/WebItem/php_session_cleanup /etc/cron.d
chmod -x /etc/cron.d/php_session_cleanup


cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/my.cnf /etc/
#jessie(20240730)-mariadb config & php ini update & 00-mpm.conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/mariadb-server.cnf /etc/my.cnf.d/
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/php.ini /etc/opt/remi/php82/php.ini
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/00-mpm.conf /etc/httpd/conf.modules.d/00-mpm.conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/httpd.conf /etc/httpd/conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/ssl.conf /etc/httpd/conf.d/
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/ca.crt /etc/httpd/conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/server.crt /etc/httpd/conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/server.key /etc/httpd/conf
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/sudoers /etc/
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/htaccess /var/www/html/.htaccess
systemctl stop php82-php-fpm.service
cp -rf /mnt/119/5-AcroStor-Fedora/install/WebItem/ui/* /var/www/html
mkdir /var/www/html/check_update
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/list_version.sh /var/www/html/check_update/
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/update_button_wget_action.sh /var/www/html/check_update/update_button_action.sh
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/update_progress.sh /var/www/html/check_update/
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/check_button_wget_action.sh /var/www/html/check_update/check_button_action.sh
# cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/swversion.dat /var/www/html/check_update/
cp -f /mnt/119/5-AcroStor-Fedora/source/xor/xor  /var/www/html/check_update/
cp -f /mnt/119/5-AcroStor-Fedora/install/config.txt /var/www/html/
cp -f /mnt/119/5-AcroStor-Fedora/install/SQLProcedure/*.sql /root/art
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/TestGtk.exe.config /var/www/html
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/TestGtk.tar.gz /var/www/html
cp -f /var/www/html/script/date.sh /var/www/html
chown -R apache:apache /var/www/html/webapi
cp -f /mnt/119/5-AcroStor-Fedora/install/WebItem/ui.config /var/www/html
chown apache:apache /var/www/html/ui.config

# ********************************************************
# . /mnt/119/5-AcroStor-Fedora/install/install_web.sh 1  <---
# ********************************************************
chown mysql:mysql /var/lib/mysql

cp -f /mnt/119/5-AcroStor-Fedora/install/multipath.conf /etc/
cp -f /mnt/119/5-AcroStor-Fedora/install/debug.txt /root/art/

# cp -f /mnt/119/5-AcroStor-Fedora/install/iscsid.conf /etc/iscsi/
cp -f /mnt/119/5-AcroStor-Fedora/install/config.txt /var/www/html/config.txt
# 應該要分firmware版本
cp -f /mnt/119/5-AcroStor-Fedora/upload/model_config/fw_config_Acro-ANS.txt /var/www/html/fw_config.txt
cp -f /mnt/119/5-AcroStor-Fedora/upload/model_config/machine_Acro-ANS.config /var/www/html/check_update/machine.config
cp -f /mnt/119/5-AcroStor-Fedora/upload/model_config/swversion_Acro-ANS.dat /var/www/html/check_update/swversion.dat
echo "ignore" > /var/www/html/check_update/update_id.dat

cp -f /mnt/119/5-AcroStor-Fedora/install/rc_zfs.local /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local

useradd artalk 
mkdir /home/artalk/.ssh
cp /mnt/119/5-AcroStor-Fedora/install/authorized_keys /home/artalk/.ssh/
chown -R artalk:artalk /home/artalk/.ssh
chmod 700 /home/artalk/.ssh
chmod -x /home/artalk/.ssh/authorized_keys
mkdir /root/.ssh
chmod 700 /root/.ssh
cp -f /mnt/119/5-AcroStor-Fedora/install/id_rsa_vdi /root/.ssh/id_rsa
cp -f /mnt/119/5-AcroStor-Fedora/install/id_rsa_vdi.pub /root/.ssh/id_rsa.pub
cp -f /mnt/119/5-AcroStor-Fedora/install/authorized_keys_cpm /root/.ssh/authorized_keys
ln -s /storage/ceph/system/known_hosts /root/.ssh/known_hosts
chmod -R 700 /root/.ssh

#set acpi
	# cp -f /mnt/119/5-AcroStor-Fedora/install/powerconf /etc/acpi/events/powerconf
	# chmod +r /etc/acpi/events/powerconf
	# systemctl start acpid.service
	# systemctl enable acpid.service
	# cp -f /mnt/119/5-AcroStor-Fedora/install/logind.conf /etc/systemd/logind.conf

cp -f /mnt/119/5-AcroStor-Fedora/source/udp_serv/udp_serv.exe /sbin/udp_serv.exe
chmod +x /sbin/udp_serv.exe

# test ---->
mkdir /etc/sysconfig/modules
# test <---
cp -f /mnt/119/5-AcroStor-Fedora/install/bluez-uinput.modules /etc/sysconfig/modules/bluez-uinput.modules
chmod +x /etc/sysconfig/modules/bluez-uinput.modules
cp -f /mnt/119/5-AcroStor-Fedora/install/script/bluez-uinput.sh /etc/sysconfig/bluez-uinput.sh
chmod +x /etc/sysconfig/bluez-uinput.sh
cp -f /mnt/119/5-AcroStor-Fedora/source/ddsn/ddsn_2 /sbin/ddsn_2
chmod +x /sbin/ddsn_2

mkdir /mnt/24
mount -t cifs //192.168.90.24/RD_Share /mnt/24 -o username=charles_lin,password=000000
mkdir /root/art/gateway
cp -rf /mnt/24/Acro_Gateway/AcroGateway/* /root/art/gateway/

echo '# create new line' > /etc/modprobe.d/kvm-nested.conf
echo 'options kvm_intel nested=1' >> /etc/modprobe.d/kvm-nested.conf

# ##########################
# for art_setup.sh
# ##########################
cp -f /mnt/119/5-AcroStor-Fedora/install/ghost/clear_nic.sh      /root/art/script/
cp -f /mnt/119/5-AcroStor-Fedora/install/ghost/before_ghost.sh   /root/art/script/

# #######################
# Install ctdb & samba
# #######################
mkdir /root/art/samba
# ? 未測試是否需要
# ? cp /mnt/119/5-AcroStor-Fedora/install/ctdb.conf /etc/ctdb/ctdb.conf
cp -f /mnt/119/5-AcroStor-Fedora/install/script/samba/* /root/art/samba/.
cp -f /mnt/119/5-AcroStor-Fedora/install/script/samba/smb.conf /etc/samba/.
# ? cp /mnt/119/5-AcroStor-Fedora/install/nsswitch.conf /etc/.
# ? cp /usr/sbin/lspci /usr/sbin/lspci.bin
# ? cp /mnt/119/5-AcroStor-Fedora/install/lspci /usr/sbin/.

# #######################
# initial firewall
# #######################
/var/www/html/script/firewall-ctl.sh initial

echo "1" > /var/www/html/fw_develop.txt

