#!/bin/bash
set -ex
function cleanup {
    set +ex
}
trap cleanup EXIT

python -c 'import sys; sys.exit(0 if (sys.version_info[0] > 2 and sys.platform in ("linux", "linux2")) else 1)'

ISSUE=$(cat /etc/issue | head -n 1)

if [[ "$ISSUE" != "Debian"* ]] && [[ "$ISSUE" != "Ubuntu"* ]] ; then
    exit 1
fi

if [ -t 1 ] ; then
    reset
fi

apt-get update && apt-get install -yy apt-utils

apt-get install -yy \
    gcc \
    unzip \

apt-get install -yy \
    apache2-utils \
    clang \
    dnsutils \
    emacs \
    gdb \
    htop \
    jq \
    less \
    lldb \
    man \
    moreutils \
    mosh \
    ncdu \
    net-tools \
    netcat \
    psmisc \
    silversearcher-ag \
    socat \
    strace \
    tcpdump \
    tmux \
    vim \
    zip \

pip install --upgrade pip virtualenv

touch ~/.tmux.conf
if ! grep -q mode-keys ~/.tmux.conf ; then
    echo "setw -g mode-keys vi" >> ~/.tmux.conf
fi
if ! grep -q status-keys ~/.tmux.conf ; then
    echo "set -g status-keys vi" >> ~/.tmux.conf
fi
if ! grep -q escape-time ~/.tmux.conf ; then
    echo "set -sg escape-time 0" >> ~/.tmux.conf
fi

touch ~/.vimrc
if ! grep -q 'set number' ~/.vimrc ; then
    echo "set number" >> ~/.vimrc
fi
if ! grep -q 'syntax' ~/.vimrc ; then
    echo "syntax on" >> ~/.vimrc
fi

if ! grep -q 'TERM=' ~/.bashrc ; then
    export TERM=screen-256color
    echo 'TERM=screen-256color' >> ~/.bashrc
fi

if [ ! -f ~/.bash_profile ] ; then
    cat << 'EOF' > ~/.bash_profile
if [ -f ~/.bashrc ]; then
   source ~/.bashrc
fi
EOF
fi

touch ~/.bashrc

if [ ! -d ~/.pyenv ] ; then
    git clone 'https://www.github.com/pyenv/pyenv' ~/.pyenv
    cat << 'EOF' > ~/.bashrc
if command -v [[ > /dev/null ; then
    if ! command -v pyenv > /dev/null ; then
        export PATH="~/.pyenv/bin:$PATH"
        eval "$(~/.pyenv/bin/pyenv init -)"
    fi
fi
EOF
fi

set +ex
