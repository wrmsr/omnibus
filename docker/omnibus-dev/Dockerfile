FROM ubuntu:eoan-20200608
COPY .dockertimestamp /


# Packages

RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-utils

RUN ( \
  apt-get install -y \
\
    aria2 \
    build-essential \
    curl \
    dnsutils \
    dumb-init \
    gcc \
    gdb \
    git \
    htop \
    iputils-ping \
    iputils-tracepath \
    jq \
    less \
    libpq-dev \
    libsnappy-dev \
    make \
    man \
    moreutils \
    nano \
    ncdu \
    net-tools \
    netcat \
    nginx \
    perl \
    pkg-config \
    postgresql-client \
    python \
    silversearcher-ag \
    socat \
    software-properties-common \
    strace \
    sudo \
    tcpdump \
    tmux \
    unzip \
    vim \
    wget \
    zip \
\
)

RUN echo "\n\n" >> ~/.bashrc


# Python build

RUN apt-get build-dep -y python3

RUN ( \
  apt-get install -y \
\
    libbz2-dev \
    libdb5.3-dev \
    libexpat1-dev \
    libffi-dev \
    libgdbm-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    uuid-dev \
    zlib1g-dev \
\
)


# JDK

RUN ( \
  add-apt-repository ppa:openjdk-r/ppa && \
  apt-get update && \
  apt-get install -y openjdk-8-jdk openjdk-14-jdk \
)

RUN ( \
  # https://stackoverflow.com/questions/6784463/error-trustanchors-parameter-must-be-non-empty \
  /usr/bin/printf '\xfe\xed\xfe\xed\x00\x00\x00\x02\x00\x00\x00\x00\xe2\x68\x6e\x45\xfb\x43\xdf\xa4\xd9\x92\xdd\x41\xce\xb6\xb2\x1c\x63\x30\xd7\x92' > /etc/ssl/certs/java/cacerts && \
  /var/lib/dpkg/info/ca-certificates-java.postinst configure \
)


# rustup

RUN ( \
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
  echo "\
source ~/.cargo/env \n\
\n\
  " >> ~/.bashrc \
)


# pyenv

RUN ( \
  cd ~ && git clone https://github.com/pyenv/pyenv .pyenv && \
  echo "\
PYENV_ROOT=~/.pyenv \n\
PATH=\"~/.pyenv/bin:\$PATH\" \n\
\n\
  " >> ~/.bashrc \
)


# jp

RUN ( \
  wget https://github.com/jmespath/jp/releases/download/0.1.3/jp-linux-amd64 -O /usr/local/bin/jp && \
  chmod +x /usr/local/bin/jp \
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


# Entrypoint

WORKDIR /omnibus

ENTRYPOINT ["dumb-init", "--"]

CMD ["sh", "-c", "echo 'Ready' && sleep infinity"]
