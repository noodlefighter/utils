
ARCH         ?= arm
CROSS        ?= /home/mpc/lichee/nano/build/nano/host/bin/arm-nano-linux-musleabi-
LINUX_ROOT   ?= /home/mpc/lichee/nano/linux/

obj-m             += example-module.o
example-module-y  += some-other-file.o

default:
	@make -C $(LINUX_ROOT) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS) M=$(PWD) modules

clean:
	@make -C $(LINUX_ROOT) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS) M=$(PWD) clean
