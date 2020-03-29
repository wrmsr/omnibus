DOCKER_USER=wrmsr

DOCKER_IMAGES:= \
	omnibus-dev \
	omnibus-mysql \
	omnibus-postgres \
	omnibus-redis \

DOCKER_COMPOSE_SERVICES:= \
	omnibus-dev \
	omnibus-mysql-master \
	omnibus-mysql-slave \
	omnibus-postgres-master \
	omnibus-postgres-slave \
	omnibus-redis \

.PHONY: all
all: clean images

define do-image
	(cd .. && docker build --tag "$(DOCKER_USER)/$1" -f "docker/$1/Dockerfile" .)
endef

define do-clean
	docker-compose rm -fv $1
endef

.PHONY: images
images:
	for IMG in $(DOCKER_IMAGES) ; do \
		$(call do-image,$$IMG) ; \
	done

.PHONY: clean
clean: stop
	for SVC in $(DOCKER_COMPOSE_SERVICES) ; do \
		$(call do-clean,$$SVC) ; \
	done

.PHONY: start
start:
	docker-compose start

.PHONY: stop
stop:
	docker-compose stop

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: reup
reup: clean images up

.PHONY: enable-ptrace
enable-ptrace:
	docker run --privileged -it python:3 sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
