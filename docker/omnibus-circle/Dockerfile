FROM python:3.8.5-buster
COPY .dockertimestamp /

RUN \
    touch ~/.bashrc && \
    echo 'export CIRCLECI=true' >> ~/.bashrc \
;

RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-utils

RUN ( \
  apt-get install -y \
\
    build-essential \
    dumb-init \
    gcc \
    gdb \
    git \
    less \
    libpq-dev \
    libsnappy-dev \
    make \
    moreutils \
    pkg-config \
    silversearcher-ag \
    socat \
    software-properties-common \
    strace \
    sudo \
    tmux \
    unzip \
    vim \
    wget \
    zip \
\
)

RUN mkdir /build
WORKDIR /build

COPY requirements.txt /build/requirements.txt
COPY requirements-dev.txt /build/requirements-dev.txt
RUN pip install --quiet --progress-bar=off -r requirements-dev.txt

RUN mkdir /omnibus
COPY . /omnibus/

WORKDIR /omnibus

CMD ["bash", "-c", "make circle-test"]
