FROM mysql:8.0.20
COPY .dockertimestamp /

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 5072E1F5

RUN ( \
  apt-get -o Acquire::Check-Valid-Until=false update && \
  apt-get install -y \
    apt-utils \
    iputils-ping \
    sudo \
    tmux \
    vim \
)

RUN ( \
    echo "root ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "mysql ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
)

COPY docker/omnibus-mysql/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
