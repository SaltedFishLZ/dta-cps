#!/bin/bash

apt-get update && \
apt-get install -yqq vim wget unzip curl gawk git && \
apt-get update && \
apt-get install -yqq autoconf automake autotools-dev \
    libmpc-dev libmpfr-dev libgmp-dev libusb-1.0-0-dev \
    build-essential bison flex texinfo gperf \
    libtool patchutils bc zlib1g-dev \
    device-tree-compiler \
    pkg-config \
    cmake cmake-doc \
    python python3 \
    bsdmainutils && \
apt update && \
apt install -y default-jdk

# download and setup flexpret

REPO_OWNER=saltedfishlz
REPO_NAME=flexpret

git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
cd flexpret && \
git checkout RTAS14 && \
make run && \
python2 run-tests.py
