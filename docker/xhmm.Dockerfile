# 
# Build script for a docker container containing XHMM
#
# author: Paweł Sztromwasser
#
FROM dpipe/common:latest

##############
#### XHMM version, download url, and install directory 
#### NOTE: the install root dir must contain bin subdir that is in the PATH, e.g. /usr, /usr/local
#################
ENV version mar2017
ENV filename xhmm-mar2017.tgz
ENV installroot /usr/local

# install dependencies first
RUN apt-get update && \
	apt-get -y install liblapack-dev

# copy the archive
COPY ${filename} ${installroot}/

# unpack, build, and make a link
RUN cd ${installroot} && \
	tar -xzf ${filename} && \
	cd xhmm-${version} && make && \
	ln -s ${installroot}/xhmm-${version}/xhmm ${installroot}/bin/xhmm

# test
RUN xhmm | true
