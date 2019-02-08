FROM ubuntu:18.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y curl sudo build-essential openjdk-8-jdk-headless fp-compiler postgresql-client python3.6 cppreference-doc-en-html cgroup-lite libcap-dev zip python3-pip libpq-dev libcups2-dev locales golang rustc mono-mcs haskell-platform
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common && add-apt-repository ppa:pypy/ppa && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y pypy3

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

#RUN curl -L https://github.com/cms-dev/cms/releases/download/v1.4.rc1/v1.4.rc1.tar.gz | tar -xz -C /
COPY . /cms

WORKDIR /cms/isolate
RUN make isolate isolate-check-environment

WORKDIR /cms
RUN python3 prerequisites.py --as-root install
RUN pip3 install -r requirements.txt && python3 setup.py install

VOLUME /data
ENTRYPOINT ./docker-entrypoint.sh
