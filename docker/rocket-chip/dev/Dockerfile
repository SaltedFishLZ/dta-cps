FROM ubuntu:18.04

ARG NCORES=16

# basic packages
# TODO: config apt source according to IP location
# some distributions may not come with `sudo`
# `sudo` will be installled later
ARG IP_LOCATION="US"

RUN apt-get update && \
    apt-get install -y sudo && \
    sudo apt-get install -y --no-install-recommends apt-utils && \
    sudo apt-get install -y vim git curl wget unzip autoconf gawk && \
    sudo apt-get update



# chipyard ubuntu dependencies
# this part comes from the Chipyard tutorial
RUN sudo apt-get install -y autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev && \
    sudo apt-get install -y libusb-1.0-0-dev gawk build-essential bison flex texinfo gperf libtool && \
    sudo apt-get install -y patchutils bc zlib1g-dev device-tree-compiler pkg-config && \
    sudo apt-get install -y libexpat-dev libfl-dev && \
    sudo apt-get install -y build-essential bison flex libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev && \
    sudo apt-get install -y gcc-5 g++-5 openjdk-8-jre openjdk-8-jdk python python3 && \
    echo "need to install apt-transport-https for some distributions. Sbt needs it" && \
    sudo apt-get install -y apt-transport-https ca-certificates && \
    sudo apt-get install -y texinfo gengetopt libexpat1-dev libusb-dev libncurses5-dev cmake perl-doc && \
    sudo apt-get install -y python3.6 patch diffstat texi2html texinfo subversion chrpath && \
    sudo apt-get install -y device-tree-compiler && \
    sudo apt-get update && \
    echo "install sbt: https://www.scala-sbt.org/release/docs/Installing-sbt-on-Linux.html" && \
    echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list && \
    curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add && \
    sudo apt-get update && \
    sudo apt-get install -y sbt




# download and install verilator
ARG VERILATOR_USE_LOCAL_PACKAGE
ARG VERILATOR_VERSION=4.008
ARG FOLDER=downloads

WORKDIR /
RUN sudo mkdir -p ${FOLDER} && \
    sudo chmod -R 777 ${FOLDER} && \
    cd ${FOLDER} && \
    curl -LO https://www.veripool.org/ftp/verilator-${VERILATOR_VERSION}.tgz && \
    tar -xvzf verilator-${VERILATOR_VERSION}.tgz && \
    cd verilator-${VERILATOR_VERSION} && \
    autoconf && ./configure && \
    make -j${NCORES} && \
    make test && \
    sudo make install




# download rocket-tools
ARG REPO_OWNER=saltedfishlz
ARG REPO_NAME=rocket-tools
ARG RISCV=/opt/riscv
ENV PATH=${RISCV}:${PATH}

WORKDIR /
RUN git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
    cd ${REPO_NAME} && \
    git submodule update --init --recursive && \
    export RISCV=$RISCV && \
    export MAKEFLAGS=-j${NCORES} && \
    ./build.sh && \
    ./build-rv32ima.sh




# download rocket-chip
# release 1.2
ARG REPO_OWNER=saltedfishlz
ARG REPO_NAME=rocket-chip


WORKDIR /
RUN git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
    cd ${REPO_NAME} && \
    git submodule update --init --recursive && \
    git checkout master && \
    cd emulator && \
    make -j${NCORES} && \
    make -j${NCORES} run-asm-tests && \
    make -j${NCORES} run-bmark-tests && \
    make -j${NCORES} debug && \
    make -j${NCORES} CONFIG=DefaultRV32Config && \
    make -j${NCORES} CONFIG=DefaultRV32Config run-asm-tests && \
    make -j${NCORES} CONFIG=DefaultRV32Config run-bmark-tests && \
    make -j${NCORES} CONFIG=DefaultRV32Config debug; \
    make clean
