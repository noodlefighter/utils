# options and settings
PROJECT	?= test

# app staticlib sharedlib
TEMPLATE ?= app

#
# available OPT:
# 0 - 3: low optimization - high optimization
# s: size optimization
# fast
OPT	= s

USE_STATIC_BUILD = no
USE_DEBUG = no

# list options
USE_LIST_OUTPUT = no

# directory define
PRJDIR   = .
SRCDIR   = $(PRJDIR)
OBJ_DIR ?= obj

# User source files/includes/macros
# add .c source files to USR_SRCS
# add .h header files to USR_INCS
# add pre-defines to USR_DEFS
# add library directory to USR_LIBS
USR_DEFS +=

# cross compile
#TCHAIN   ?= arm-none-eabi-
#SYSROOT  ?= /usr
#USR_INCS += ${SYSROOT}/include

# pkg-config packages depends on
pkg_packages :=

USR_LIBS += -lpthread -ldl -lm -lstdc++

# app
VPATH    += $(SRCDIR)
USR_INCS += $(SRCDIR)
USR_SRCS += $(wildcard $(SRCDIR)/*.c)

# User can add custom target like:
# default_target: custom_target all
# custom_target:
# 	touch $@ 

# include common
include common.mk
