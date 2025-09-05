#!/bin/sh

mkdir /mnt/119
mount1; mount -t cifs //192.168.88.119/thttpd  /mnt/119 -o username=thttpd,password=thttpd

mkdir -p /var/www/html/script
mkdir /var/www/html/updateFilePath
mkdir /mnt/tmpfs
mkdir -p /root/art/script
mkdir /etc/cron.d
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/selinux.config /etc/selinux/config
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/environment /etc/environment


cd /root
mkdir /storage
mkdir /artgluster
useradd -M -s /sbin/nologin -g nobody -d /storage/gfs1/manager manager 
cd /root
echo acrored > m.pwd
echo acrored >> m.pwd
cat m.pwd | pdbedit -a manager
rm -f m.pwd

cp -f /mnt/119/3-VDI-CEPH-HTTP/install/script/*.sh /var/www/html/script

# ====================================================
# install_web_fc37_hci.sh 1 --->
# ====================================================
mkdir -p /LocalDB/admin/session
mkdir -p /LocalDB/admin/session
mkdir -p /LocalDB/manager/session
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/config.pwd /LocalDB/config.pwd
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/pwd /LocalDB/admin/pwd
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/slat /LocalDB/admin/slat
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/pwd /LocalDB/manager/pwd
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/slat /LocalDB/manager/slat
chown -R apache:apache /LocalDB
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/php5 /etc/cron.d
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/mysql-bk /etc/cron.d
chmod -x /etc/cron.d/php5
chmod -x /etc/cron.d/mysql-bk
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/my.cnf /etc/
#jessie(20230208)-mariadb config & php ini update
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/mariadb-server.cnf /etc/my.cnf.d/
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/php.ini /etc/opt/remi/php82/php.ini
# rm -f /etc/php.ini
# ln -s /etc/opt/remi/php82/php.ini /etc/php.ini
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/00-mpm.conf /etc/httpd/conf.modules.d/00-mpm.conf
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/httpd.conf /etc/httpd/conf
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/ssl.conf /etc/httpd/conf.d/
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/ca.crt /etc/httpd/conf
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/server.crt /etc/httpd/conf
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/server.key /etc/httpd/conf
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/sudoers /etc/
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/htaccess /var/www/html/.htaccess
cp -rf /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/ui/* /var/www/html
systemctl restart httpd
systemctl stop php82-php-fpm.service
mkdir /var/www/html/check_update
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/list_version.sh /var/www/html/check_update/
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/update_button_wget_action.sh /var/www/html/check_update/update_button_action.sh
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/update_progress.sh /var/www/html/check_update/
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/check_button_wget_action.sh /var/www/html/check_update/check_button_action.sh
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/swversion.dat /var/www/html/check_update/
cp /mnt/119/3-VDI-CEPH-HTTP/source/xor/xor  /var/www/html/check_update/
cp /mnt/119/3-VDI-CEPH-HTTP/install/config.txt /var/www/html/
cp /mnt/119/3-VDI-CEPH-HTTP/install/SQLProcedure/*.sql /root/art
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/TestGtk.exe.config /var/www/html
cp /mnt/119/3-VDI-CEPH-HTTP/install/WebItem/TestGtk.tar.gz /var/www/html
cp /var/www/html/script/date.sh /var/www/html
chown -R apache:apache /var/www/html/webapi
# ====================================================
# install_web_fc37_hci.sh 1 --->
# ====================================================

cp -f /mnt/119/3-VDI-CEPH-HTTP/install/multipath.conf /etc/
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/debug.txt /root/art/

cp -f /mnt/119/3-VDI-CEPH-HTTP/install/iscsid.conf /etc/iscsi/
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/config.txt /var/www/html/config.txt
# 應該要分firmware版本
cp -f /mnt/119/3-VDI-CEPH-HTTP/upload/model_config/fw_config_Acro-HCI.txt /var/www/html/fw_config.txt
cp -f /mnt/119/3-VDI-CEPH-HTTP/upload/model_config/machine_Acro-HCI.config /var/www/html/check_update/machine.config
cp -f /mnt/119/3-VDI-CEPH-HTTP/upload/model_config/swversion_Acro-HCI.dat /var/www/html/check_update/swversion.dat
echo "ignore" > /var/www/html/check_update/update_id.dat

cp -f /mnt/119/3-VDI-CEPH-HTTP/install/rc_zfs.local /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local

useradd artalk 
mkdir /home/artalk/.ssh
cp /mnt/119/3-VDI-CEPH-HTTP/install/authorized_keys /home/artalk/.ssh/
chown -R artalk:artalk /home/artalk/.ssh
chmod 700 /home/artalk/.ssh
chmod -x /home/artalk/.ssh/authorized_keys
mkdir /root/.ssh
chmod 700 /root/.ssh
cp /mnt/119/3-VDI-CEPH-HTTP/install/id_rsa_vdi /root/.ssh/id_rsa
cp /mnt/119/3-VDI-CEPH-HTTP/install/id_rsa_vdi.pub /root/.ssh/id_rsa.pub
cp /mnt/119/3-VDI-CEPH-HTTP/install/authorized_keys_cpm /root/.ssh/authorized_keys
ln -s /storage/ceph/system/known_hosts /root/.ssh/known_hosts
chmod -R 700 /root/.ssh


#set acpi
# yum -y install acpid
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/powerconf /etc/acpi/events/powerconf
chmod +r /etc/acpi/events/powerconf
systemctl restart acpid.service
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/logind.conf /etc/systemd/logind.conf

cp -f /mnt/119/3-VDI-CEPH-HTTP/source/udp_serv/udp_serv.exe /sbin/udp_serv.exe
chmod +x /sbin/udp_serv.exe


# 沒有產生 /etc/sysconfig/encode檔, 所以是沒有鎖碼狀態
# cp -f /mnt/119/3-VDI-CEPH-HTTP/install/bluez-uinput.modules /etc/sysconfig/modules/bluez-uinput.modules
# chmod +x /etc/sysconfig/modules/bluez-uinput.modules
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/script/bluez-uinput.sh /etc/sysconfig/bluez-uinput.sh
chmod +x /etc/sysconfig/bluez-uinput.sh

cp -f /mnt/119/3-VDI-CEPH-HTTP/source/ddsn/ddsn_2 /sbin/ddsn_2
chmod +x /sbin/ddsn_2
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/script/newsn.sh /etc/sysconfig/newsn.sh
chmod +x /etc/sysconfig/newsn.sh

# 2019/10/17 --->
# ================
rm -f /etc/ssmtp/ssmtp.conf
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/iscsid.conf /root/art/
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/sshd_config /etc/ssh/sshd_config
mkdir /mnt/24
mount -t cifs //192.168.90.24/RD_Share /mnt/24 -o username=charles_lin,password=000000
mkdir /root/art/gateway
cp -rf /mnt/24/Acro_Gateway/AcroGateway/* /root/art/gateway/

systemctl stop rsyslog.service
systemctl disable rsyslog.service
auditctl -e 0
systemctl disable auditd.service
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/journald.conf /etc/systemd/journald.conf

###### For VGA Passthrough ######
cp -f /mnt/119/3-VDI-CEPH-HTTP/install/idv.conf /root/art
cp -f /mnt/119/3-VDI-CEPH-HTTP/upload/model_config/ui_Acro7-HCI.config /var/www/html/ui.config

systemctl start firewalld.service
/var/www/html/script/firewall-ctl.sh initial
mkdir /var/www/html/updateUpload
echo '# create new line' > /etc/modprobe.d/kvm-nested.conf
echo 'options kvm_intel nested=1' >> /etc/modprobe.d/kvm-nested.conf

# #####################
# new action 2019120301
# #####################
/var/www/html/script/0genAccount.sh

# ##########################
# for art_setup.sh
# ##########################
mkdir /root/art/script
cp /mnt/119/3-VDI-CEPH-HTTP/install/ghost/clear_nic.sh      /root/art/script/
cp /mnt/119/3-VDI-CEPH-HTTP/install/ghost/before_ghost.sh   /root/art/script/

echo 'user = "root"' >> /etc/libvirt/qemu.conf
echo 'group = "root"' >> /etc/libvirt/qemu.conf

echo "1" > /var/www/html/fw_develop.txt
