FROM ubuntu:18.04

ARG NCORES=16


# config apt source according to IP location
ARG IP_LOCATION="US"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update



# basic packages
RUN apt-get install -yq vim sudo git curl wget unzip autoconf gawk && \
    apt-get update && \
    apt-get install -yq dialog && \
    apt-get install -yq debconf-utils apt-utils && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y keyboard-configuration && \
    dpkg --configure -a && \
    echo "need to install apt-transport-https for some distributions." && \
    echo "non-official apt packages need it" && \
    apt-get install -yq apt-transport-https ca-certificates


# chipyard ubuntu dependencies
# this part comes from the Chipyard tutorial
RUN sudo apt-get install -yq build-essential bison flex libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev && \
    sudo apt-get install -yq gcc-5 g++-5 openjdk-8-jre openjdk-8-jdk python python3


# install sbt: https://www.scala-sbt.org/release/docs/Installing-sbt-on-Linux.html
RUN echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
RUN curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add
RUN sudo apt-get update && \
    sudo apt-get install -yq sbt


# ubuntu 16.04 cannot find package python3.6
RUN sudo apt-get install -y texinfo gengetopt libexpat1-dev libusb-dev libncurses5-dev cmake perl-doc && \
    echo "deps for poky" && \
    sudo apt-get install -y python3.6 patch diffstat texi2html texinfo subversion chrpath && \
    echo "deps for qemu" && \
    DEBIAN_FRONTEND=noniteractive sudo apt-get install -y libgtk-3-dev gettext && \
    echo "deps for firemarshal" && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python3.6-dev rsync libguestfs-tools expat ctags && \
    echo "install DTC" && \
    DEBIAN_FRONTEDN=noninteractive apt-get install -y device-tree-compiler && \
    sudo apt-get update 





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
# 1.1.0
ARG REPO_HASH=7a6124d462b211f7123b1307a27aa125cf90134b


WORKDIR /
RUN git clone https://github.com/${REPO_OWNER}/${REPO_NAME}.git && \
    cd ${REPO_NAME} && \
    git checkout ${REPO_HASH} && \
    ./scripts/init-submodules-no-riscv-tools.sh
#     export MAKEFLAGS=-j${NCORES} && \
#     export CC=gcc-5 CXX=g++-5  && \
#     ./scripts/build-toolchains.sh riscv-tools


# WORKDIR /${REPO_NAME}
# RUN git checkout ${REPO_HASH}
# RUN ./scripts/init-submodules-no-riscv-tools.sh
# RUN export MAKEFLAGS=-j${NCORES}
# # for a normal risc-v toolchain
# RUN ./scripts/build-toolchains.sh riscv-tools



WORKDIR /
