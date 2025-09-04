#!/bin/bash
dnf -y install --skip-broken epel-release gcc make autoconf automake libtool rpm-build libtirpc-devel libblkid-devel libuuid-devel libudev-devel openssl-devel zlib-devel libaio-devel libattr-devel elfutils-libelf-devel kernel-devel-$(uname -r) python3 python3-devel python3-setuptools python3-cffi libffi-devel git ncompress libcurl-devel

dnf -y install --skip-broken --enablerepo=epel --enablerepo=powertools python3-packaging dkms

dnf -y install git

git clone https://github.com/openzfs/zfs

cd ./zfs
git checkout master
sh autogen.sh
./configure
make -s -j$(nproc)

make rpm

make install
ldconfig
depmod

