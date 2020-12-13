FROM ubuntu:14.04



RUN apt-get update && \
    apt-get install -yqq vim wget unzip curl gawk && \
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