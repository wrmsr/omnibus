FROM ubuntu:20.04
COPY .dockertimestamp /

RUN ( \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils && \
\
    apt-get install -y \
\
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
CMD ["/home/docker-entrypoint.sh"]
