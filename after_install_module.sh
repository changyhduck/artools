#!/bin/bash
#systemctl set-default graphical.target
systemctl enable glusterfsd.service
#systemctl enable glusterd.service
systemctl enable libvirtd
#systemctl enable virtlogd
cp rc-local.service /etc/systemd/system/
cp rc.local /etc/rc.d/
chmod +x /etc/rc.d/rc.local
ln -s /etc/rc.d/rc.local /etc/rc.local
systemctl enable rc-local.service
systemctl enable smb
systemctl enable nmb
systemctl enable acpid
grubby --update-kernel ALL --args selinux=0
reboot