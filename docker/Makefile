DOCKER_USER=wrmsr

DOCKER_IMAGES:= \
	omnibus-dev \
	omnibus-elasticsearch \
	omnibus-kafka \
	omnibus-memcached \
	omnibus-minio \
	omnibus-mongo \
	omnibus-mysql \
	omnibus-postgres \
	omnibus-redis \
	omnibus-spark-master \
	omnibus-spark-worker \
	omnibus-zookeeper \

DOCKER_COMPOSE_DEFAULT_SERVICES:= \
	omnibus-mysql-master \
	omnibus-mysql-slave \
	omnibus-postgres-master \
	omnibus-postgres-slave \
	omnibus-redis \

DOCKER_COMPOSE_SERVICES:= \
	$(DOCKER_COMPOSE_DEFAULT_SERVICES) \
	omnibus-elasticsearch \
	omnibus-kafka \
	omnibus-memcached \
	omnibus-minio \
	omnibus-mongo \
	omnibus-spark-master \
	omnibus-spark-worker \
	omnibus-zookeeper \

.PHONY: all
all: clean images

define do-image
	(cd .. && docker build --tag "$(DOCKER_USER)/$1" -f "docker/$1/Dockerfile" .)
endef

define do-clean
	docker-compose rm -fv $1
endef

.PHONY: clean-services
clean-services: stop
	for SVC in $(DOCKER_COMPOSE_SERVICES) ; do \
		$(call do-clean,$$SVC) ; \
	done

.PHONY: clean
clean: clean-services
	$(call do-clean,omnibus-dev)

.PHONY: images
images:
	for IMG in $(DOCKER_IMAGES) ; do \
		$(call do-image,$$IMG) ; \
	done
	$(call do-image,omnibus-dev)

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

.PHONY: rmdev
rmdev:
	docker-compose rm -sf omnibus-dev

.PHONY: reup
reup: stop
	docker-compose rm -sf $(DOCKER_COMPOSE_SERVICES)
	$(MAKE) clean-services images
	docker-compose up --no-recreate $(DOCKER_DEFAULT_COMPOSE_SERVICES) omnibus-dev

.PHONY: enable-ptrace
enable-ptrace:
	docker run --privileged -it python:3 sh -c 'echo 0 > /proc/sys/kernel/yama/ptrace_scope'
