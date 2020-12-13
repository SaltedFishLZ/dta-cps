#!/bin/bash

# when necessary, please use sudo

export NCORES=16

apt-get update

apt-get install -yqq vim sudo git curl wget unzip autoconf gawk && \
apt-get update && \
apt-get install -yqq dialog && \
apt-get install -yqq debconf-utils && \
apt-get install -yqq --no-install-recommends apt-utils && \
apt-get install -yqq keyboard-configuration && \
sudo dpkg --configure -a && \
sudo apt-get install -yqq locales && \
apt-get update


sudo apt-get install -yqq build-essential bison flex libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev && \
sudo apt-get install -yqq gcc-5 g++-5 openjdk-8-jre openjdk-8-jdk python python3 && \
echo "need to install apt-transport-https for some distributions." && \
echo "non-official apt packages need it" && \
apt-get install -yqq apt-transport-https ca-certificates


echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
sudo apt-get update && \
sudo apt-get install -yqq sbt



sudo apt-get install -yqq texinfo gengetopt libexpat1-dev libusb-dev libncurses5-dev cmake perl-doc && \
echo "deps for poky" && \
sudo apt-get install -yqq python3.6 patch diffstat texi2html texinfo subversion chrpath && \
echo "deps for qemu" && \
sudo apt-get install -yqq libgtk-3-dev gettext && \
echo "deps for firemarshal" && \
sudo apt-get install -yqq python3-pip python3.6-dev rsync libguestfs-tools expat ctags && \
echo "install DTC" && \
sudo apt-get install -yqq device-tree-compiler && \
sudo apt-get update





VERILATOR_VERSION=4.034
FOLDER=downloads

sudo mkdir -p ${FOLDER} && \
sudo chmod -R 777 ${FOLDER} && \
cd ${FOLDER} && \
curl -LO https://www.veripool.org/ftp/verilator-${VERILATOR_VERSION}.tgz && \
tar -xvzf verilator-${VERILATOR_VERSION}.tgz && \
cd verilator-${VERILATOR_VERSION} && \
autoconf && ./configure && \
make -j${NCORES} && \
make test && \
sudo make install
cd /


# download and install chipyard
# using too many cores may cause memory overflow, be careful
CHIPYARD_USE_LOCAL_PACKAGE=True
REPO_OWNER=ucb-bar
REPO_NAME=chipyard

# 1.3.0
REPO_HASH=c576a7e76717376b7a2cbbc0a531f51382ff87f1


git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
cd ${REPO_NAME} && \
git checkout ${REPO_HASH} && \
./scripts/init-submodules-no-riscv-tools.sh


# incompatible with export CC=gcc-5 CXX=g++-5
export MAKEFLAGS=-j${NCORES} && \
./scripts/build-toolchains.sh riscv-tools



echo "export CPATH=\${RISCV}/include" >> env-riscv-tools.sh
echo "export LIBRARY_PATH=\${RISCV}/lib\${LIBRARY_PATH:+:\${LIBRARY_PATH}}" >> env-riscv-tools.sh