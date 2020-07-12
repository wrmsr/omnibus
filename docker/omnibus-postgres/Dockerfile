FROM postgres:12.3
COPY .dockertimestamp /

RUN ( \
  apt-get -o Acquire::Check-Valid-Until=false update && \
  apt-get install -y \
    apt-utils \
    build-essential \
    ca-certificates \
    curl \
    gcc \
    git-core \
    iputils-ping \
    make \
    postgresql-server-dev-12 \
    python \
    tmux \
    vim \
    wget \
)

COPY docker/omnibus-postgres/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


# RUN ( \
#   mkdir /build && \
#   cd /build && \
#   wget https://github.com/eulerto/wal2json/archive/wal2json_2_2.tar.gz && \
#   tar xvzf wal2json_2_2.tar.gz && \
#   cd wal2json-wal2json_2_2 && \
#   export PATH=pg_config:$PATH && \
#   USE_PGXS=1 make && \
#   USE_PGXS=1 make install \
# )


# ENV \
#   PLV8_VERSION=v2.1.0 \
#   PLV8_SHASUM="8a05f9d609bb79e47b91ebc03ea63b3f7826fa421a0ee8221ee21581d68cb5ba  v2.3.5.tar.gz"
#
# RUN ( \
#   mkdir -p /tmp/build && \
#   curl -o /tmp/build/${PLV8_VERSION}.tar.gz -SL "https://github.com/plv8/plv8/archive/$PLV8_VERSION.tar.gz" && \
#   cd /tmp/build && \
#   echo ${PLV8_SHASUM} | sha256sum -c && \
#   tar -xzf /tmp/build/${PLV8_VERSION}.tar.gz -C /tmp/build/ && \
#   cd /tmp/build/plv8-${PLV8_VERSION#?} && \
#   sed -i 's/\(depot_tools.git\)/\1; cd depot_tools; git checkout 46541b4996f25b706146148331b9613c8a787e7e; rm -rf .git;/' Makefile.v8 && \
#   make -j static && \
#   make install \
# )
