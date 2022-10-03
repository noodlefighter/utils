
IMG_NAME=ebsx-dev-env
DIR_WORK=$(shell pwd)/..

all: help

help:
	@echo "usage: make { build | up | down | ssh | clean }"

build:
	mkdir -p ./tmp
	cp $(HOME)/.ssh/id_rsa.pub ./tmp/
	docker build -t $(IMG_NAME) .

up:
	docker run -e LOCAL_USER_ID=$(shell id -u $$USER) -itd \
		--mount type=bind,source=$(DIR_WORK)/linux,target=/home/vagrant/MYiR-iMX-Linux \
		--mount type=bind,source=$(DIR_WORK)/uboot,target=/home/vagrant/MYiR-iMX-Uboot \
		--mount type=bind,source=$(DIR_WORK)/workspace,target=/home/vagrant/workspace \
		--mount type=bind,source=$(DIR_WORK)/yocto,target=/home/vagrant/yocto \
		--name $(IMG_NAME) \
		$(IMG_NAME) \
		/bin/bash

down:
	docker container stop $(IMG_NAME)
	docker container rm $(IMG_NAME)

ssh:
	ssh vagrant@$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(IMG_NAME))
	
clean:
	rm -rf tmp/
