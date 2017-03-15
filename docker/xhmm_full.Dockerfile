# 
# Build script for a docker container containing XHMM
#
# author: Paweł Sztromwasser
#
FROM ubuntu:14.04

##############
#### XHMM version, download url, and install directory 
#### NOTE: the install root dir must contain bin subdir that is in the PATH, e.g. /usr, /usr/local
#################
ENV version mar2017
ENV filename xhmm-mar2017.tgz
ENV installroot /usr/local

# install dependencies first
RUN echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty main restricted universe multiverse > /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-updates main restricted universe multiverse >> /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-backports main restricted universe multiverse >> /tmp/mirrors && \
	echo deb mirror://mirrors.ubuntu.com/mirrors.txt trusty-security main restricted universe multiverse >> /tmp/mirrors && \
	cp /etc/apt/sources.list /etc/apt/sources.list.backup && cat /tmp/mirrors /etc/apt/sources.list.backup > /etc/apt/sources.list && \
	apt-get update && \
	apt-get -y install \
		build-essential \
		liblapack-dev

# copy the archive
COPY ${filename} ${installroot}/

# unpack, build, and make a link
RUN cd ${installroot} && \
	tar -xzf ${filename} && \
	cd xhmm-${version} && make && \
	ln -s ${installroot}/xhmm-${version}/xhmm ${installroot}/bin/xhmm

# test
RUN xhmm | true
