DOCKER_USER=wrmsr

DOCKER_CIRCLE_IMAGES:= \
	omnibus-mysql \

DOCKER_IMAGES:= \
	$(DOCKER_CIRCLE_IMAGES) \
	omnibus-dev \
	omnibus-dynamodb \
	omnibus-elasticmq \
	omnibus-elasticsearch \
	omnibus-kafka \
	omnibus-memcached \
	omnibus-minio \
	omnibus-mongo \
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

.PHONY: clean-services
clean-services: stop
	for SVC in $(DOCKER_COMPOSE_SERVICES) ; do \
		docker-compose rm -fv "$$SVC" ; \
	done

.PHONY: clean
clean: clean-services
	docker-compose rm -fv omnibus-dev

.PHONY: images
images:
	for IMG in $(DOCKER_IMAGES) ; do \
		(cd .. && docker build --tag "$(DOCKER_USER)/$$IMG" -f "docker/$$IMG/Dockerfile" .) ; \
	done

.PHONY:
push:
	for IMG in $(DOCKER_IMAGES) ; do \
		docker push "$(DOCKER_USER)/$$IMG" ; \
	done

.PHONY:
pull:
	for IMG in $(DOCKER_IMAGES) ; do \
		docker pull "$(DOCKER_USER)/$$IMG" ; \
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

.PHONY: circle-images
circle-images:
	for IMG in $(DOCKER_CIRCLE_IMAGES) ; do \
		(cd .. && docker build --tag "$(DOCKER_USER)/$$IMG" -f "docker/$$IMG/Dockerfile" .) ; \
	done

	DI=$$(mktemp) ; \
	cd .. ; \
	(cat .dockerignore | egrep -v '^omnibus$$') > "$$DI" ; \
	tar cvh --exclude-from="$$DI" * .dockertimestamp | \
		docker build --tag "$(DOCKER_USER)/omnibus-circle" -f "docker/omnibus-circle/Dockerfile" -


.PHONY: circle
circle: circle-images
	docker-compose run --rm omnibus-circle
