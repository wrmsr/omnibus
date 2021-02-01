FROM ubuntu:focal-20201008
COPY .dockertimestamp /

RUN ( \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils && \
\
    apt-get install -y \
\
        apt-transport-https \
        ca-certificates \
        curl \
        dumb-init \
        gnupg-agent \
        software-properties-common \
\
)

RUN ( \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable" && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io \
)

ENTRYPOINT ["dumb-init", "--"]
CMD ["sh", "-c", "echo 'Ready' && sleep infinity"]
