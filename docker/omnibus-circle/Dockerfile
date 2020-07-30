FROM python:3.8.5-buster
COPY .dockertimestamp /


# Packages

RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list
RUN (
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
)

RUN ( \
    export DEBIAN_FRONTEND=noninteractive && \
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


# Configuration files

RUN echo "\
setw -g mode-keys vi \n\
set -g status-keys vi \n\
set -sg escape-time 0 \n\
set -g status-fg black \n\
set-option -g history-limit 20000 \n\
" >> ~/.tmux.conf

RUN echo "\
set number \n\
syntax on \n\
filetype indent plugin on \n\
" >> ~/.vimrc

RUN echo "\
TERM=screen-256color \n\
\n\
" >> ~/.bashrc

RUN echo 'source ~/.bashrc' >> ~/.bash_profile


# Circle

RUN (
    touch ~/.bashrc && \
    echo 'export CIRCLECI=true' >> ~/.bashrc \
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
