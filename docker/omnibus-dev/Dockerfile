FROM python:3.7.4

RUN \
    touch ~/.bashrc && \
    echo 'export ENV=docker_dev' > ~/.bashrc \
;

RUN mkdir /build

COPY docker/omnibus-dev/prepare_system.bash /build/prepare_system.bash
RUN /build/prepare_system.bash

WORKDIR /omnibus

CMD ["python", "-c", "import signal, subprocess, sys, os; [signal.signal(s, lambda *_: sys.exit(0)) for s in [signal.SIGTERM, signal.SIGINT]]; subprocess.Popen(['sh', '-c', 'sleep infinity']); os.wait()"]
