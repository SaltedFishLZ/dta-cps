FROM ubuntu:18.04

ARG NCORES=16


# config apt source according to IP location
ARG IP_LOCATION="US"
RUN apt-get update



# basic packages
RUN apt-get install -y vim sudo git curl wget unzip autoconf gawk && \
    apt-get update



# chipyard ubuntu dependencies
# this part comes from the Chipyard tutorial
RUN sudo apt-get install -y build-essential bison flex libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev && \
    sudo apt-get install -y gcc-5 g++-5 openjdk-8-jre openjdk-8-jdk python python3 && \
    echo "Need to install apt-transport-https for some distributions. Sbt needs it" && \
    apt-get install -y apt-transport-https ca-certificates

# install sbt: https://www.scala-sbt.org/release/docs/Installing-sbt-on-Linux.html
RUN echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
RUN sudo apt-get update && \
    sudo apt-get install -y sbt

# ubuntu 16.04 cannot find package python3.6
RUN sudo apt-get install -y texinfo gengetopt libexpat1-dev libusb-dev libncurses5-dev cmake perl-doc && \
    sudo apt-get install -y python3.6 patch diffstat texi2html texinfo subversion chrpath && \
    sudo apt-get install -y device-tree-compiler && \
    sudo apt-get update


# # deps for poky
# RUN sudo apt-get install -y python3.6 patch diffstat texi2html texinfo subversion chrpath && \
#     sudo apt-get update

# # deps for qemu
# RUN sudo apt-get install -y libgtk-3-dev gettext

# # deps for firemarshal
# RUN sudo apt-get install -y python3-pip python3.6-dev rsync libguestfs-tools expat ctags

# # install DTC
# RUN sudo apt-get install -y device-tree-compiler

# download and install verilator
ARG VERILATOR_USE_LOCAL_PACKAGE
ARG VERILATOR_VERSION=4.034
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


# RUN tar -xvzf verilator-${VERILATOR_VERSION}.tgz
# WORKDIR /downloads/verilator-${VERILATOR_VERSION}
# RUN autoconf && ./configure
# RUN make -j${NCORES}
# RUN make test
# RUN make install

# # download and install verilator
# WORKDIR /
# ARG VERILATOR_VERSION=4.034
# ARG NCORES=8
# RUN git clone http://git.veripool.org/git/verilator
# RUN cd verilator
# RUN git checkout v4.034
# RUN autoconf && ./configure
# RUN make -j16
# RUN make test
# RUN make install



# download and install chipyard
# using too many cores may cause memory overflow, be careful
ARG CHIPYARD_USE_LOCAL_PACKAGE=True
ARG REPO_OWNER=ucb-bar
ARG REPO_NAME=chipyard
# # 1.3.0
# ARG REPO_HASH=c576a7e76717376b7a2cbbc0a531f51382ff87f1
ARG REPO_HASH=32c957ce930ad283402810ddd52942d28524c3c1


WORKDIR /
RUN git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
    cd ${REPO_NAME} && \
    git checkout ${REPO_HASH} && \
    export MAKEFLAGS=-j${NCORES} && \
    export CC=gcc-5 CXX=g++-5  && \
    ./scripts/init-submodules-no-riscv-tools.sh && \
    ./scripts/build-toolchains.sh riscv-tools


# WORKDIR /${REPO_NAME}
# RUN git checkout ${REPO_HASH}
# RUN ./scripts/init-submodules-no-riscv-tools.sh
# RUN export MAKEFLAGS=-j${NCORES}
# # for a normal risc-v toolchain
# RUN ./scripts/build-toolchains.sh riscv-tools



WORKDIR /
RUN mkdir workspace