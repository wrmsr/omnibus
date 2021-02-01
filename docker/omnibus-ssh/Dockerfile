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
        dumb-init \
        openssh-server \
        python \
        vim \
\
)

RUN mkdir /var/run/sshd

RUN sed -i 's/#*PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

EXPOSE 22

COPY docker/omnibus-ssh/docker-entrypoint.sh /home
RUN chmod a+x /home/docker-entrypoint.sh

ENTRYPOINT ["dumb-init", "--"]
CMD ["/home/docker-entrypoint.sh"]
