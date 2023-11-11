DOCKER=sudo podman
CONTAINER_NAME=h3env
IMG_NAME=h3-env
DIR_WORK=$(shell pwd)/..

all: help

help:
	@echo "usage: make { build | up | down | startup | ssh | clean }"

build:
	mkdir -p ./tmp
	cp $(HOME)/.ssh/id_rsa.pub ./tmp/
	$(DOCKER) build -t $(IMG_NAME) .

up:
	$(DOCKER) run -e LOCAL_USER_ID=$(shell id -u $$USER) -itd \
		--privileged \
		--mount type=bind,source=$(DIR_WORK)/orangepi-build,target=/home/vagrant/orangepi-build \
		--name $(CONTAINER_NAME) \
		$(IMG_NAME) \
		/bin/bash

down:
	$(DOCKER) container stop $(CONTAINER_NAME)
	$(DOCKER) container rm $(CONTAINER_NAME)

startup:
	$(DOCKER) start $(CONTAINER_NAME)

ssh:
	ssh vagrant@$(shell ${DOCKER} inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(CONTAINER_NAME))

clean:
	rm -rf tmp/
