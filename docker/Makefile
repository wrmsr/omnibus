# FIXME: https://github.com/docker/compose/issues/2908 this shit is fucking stupid.
DOCKER_USER=omnibus

.PHONY: all
all: clean containers

.PHONY: containers
containers:
	(cd .. && docker build --tag $(DOCKER_USER)/omnibus-dev -f docker/omnibus-dev/Dockerfile .)
	docker-compose create

.PHONY: clean
clean: stop
	docker-compose rm -fv omnibus-dev

.PHONY: start
start:
	docker-compose start

.PHONY: stop
stop:
	docker-compose stop

.PHONY: up
up:
	docker-compose up

.PHONY: reup
reup: clean containers up

.PHONY: enable_ptrace
enable_ptrace:
	docker run --privileged -it python:3.6.3 sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
