#!/bin/bash
updatedb
usermod -G root acrored
sed -i 's/1000:1000/0:0/g' /etc/passwd
echo "acrored    ALL=(ALL)    ALL" >> /etc/sudoers
chown -R 0:0 /home/acrored
sed -i 's/ConditionUser=!root/#ConditionUser=!root/g' /usr/lib/systemd/user/pulseaudio.service
sed -i 's/ConditionUser=!root/#ConditionUser=!root/g' /usr/lib/systemd/user/pulseaudio.socket
dnf -y remove zram-generator.x86_64
echo "StrictHostKeyChecking accept-new" >> /etc/ssh/ssh_config
reboot
