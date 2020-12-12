FROM ubuntu:18.04

# config apt source according to IP location
ARG IP_LOCATION="US"
RUN apt-get update

# set up locale
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
