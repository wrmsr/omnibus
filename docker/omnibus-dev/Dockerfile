FROM ubuntu:focal-20201008
COPY .dockertimestamp /


# Packages

RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list
RUN ( \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils && \
\
    apt-get install -y \
\
        aria2 \
        bison \
        bmon \
        build-essential \
        clang \
        curl \
        cvs \
        dnsutils \
        dumb-init \
        emacs \
        firefox \
        flex \
        gcc \
        gdb \
        git \
        htop \
        iputils-ping \
        iputils-tracepath \
        jq \
        less \
        libbz2-dev \
        libdb5.3-dev \
        libexpat1-dev \
        libffi-dev \
        libgdbm-dev \
        libglib2.0-dev \
        liblzma-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libnss3-dev \
        libpcre2-dev \
        libpcre3-dev \
        libpq-dev \
        libreadline-dev \
        libsasl2-dev \
        libsnappy-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxml2-utils \
        libxslt-dev \
        llvm \
        lsof \
        make \
        man \
        mercurial \
        moreutils \
        nano \
        ncdu \
        net-tools \
        netcat \
        nginx \
        nodejs \
        npm \
        openssh-server \
        perl \
        pkg-config \
        postgresql-client \
        protobuf-compiler \
        python \
        silversearcher-ag \
        socat \
        software-properties-common \
        strace \
        subversion \
        sudo \
        tcpdump \
        telnet \
        tk-dev \
        tmux \
        unzip \
        uuid-dev \
        vim \
        vim-gtk3 \
        wget \
        x11-apps \
        xsltproc  \
        zip \
        zlib1g-dev \
        zsh \
\
)

RUN echo "\n\n" >> ~/.bashrc


# Python build

RUN apt-get build-dep -y python3 python3-tk


# JDK

RUN ( \
    add-apt-repository ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y \
    \
        openjdk-8-jdk \
        openjdk-14-jdk \
        openjdk-15-jdk \
    \
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


# js

# FIXME: https://github.com/yarnpkg/yarn/issues/8358 jfc
RUN npm install -g yarn@1.22.5


# jp

RUN ( \
    wget https://github.com/jmespath/jp/releases/download/0.1.3/jp-linux-amd64 -O /usr/local/bin/jp && \
    chmod +x /usr/local/bin/jp \
)


# Configuration

RUN ( \
    sed -i 's/^#*PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#X11UseLocalhost yes/X11UseLocalhost no/' /etc/ssh/sshd_config && \
    sed -i 's/^# Ciphers and keying/Ciphers chacha20-poly1305@openssh.com/' /etc/ssh/sshd_config && \
    sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd && \
    mkdir /var/run/sshd \
)

RUN echo "\
handle SIGUSR1 nostop noprint \n\
handle SIGUSR2 nostop noprint \n\
" >> ~/.gdbinit

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
set tabstop=4 \n\
set shiftwidth=4 \n\
set expandtab \n\
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