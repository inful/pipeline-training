# 
# Build script for a docker container with a base OS and updated package sources
#
# author: Paweł Sztromwasser
#
FROM ubuntu:14.04

RUN echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe multiverse > /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-updates main restricted universe multiverse >> /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-backports main restricted universe multiverse >> /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-security main restricted universe multiverse >> /tmp/mirrors && \
	cp /etc/apt/sources.list /etc/apt/sources.list.backup && cat /tmp/mirrors /etc/apt/sources.list.backup > /etc/apt/sources.list && \
	apt-get update && \
	apt-get -y install build-essential
