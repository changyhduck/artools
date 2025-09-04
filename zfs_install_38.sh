#!/bin/bash
rpm -e --nodeps zfs-fuse
#dnf install -y https://zfsonlinux.org/fedora/zfs-release-2-2$(rpm --eval "%{dist}").noarch.rpm
dnf install -y https://zfsonlinux.org/fedora/zfs-release-2-3$(rpm --eval "%{dist}").noarch.rpm
dnf install -y kernel-devel
dnf install -y zfs
reboot
