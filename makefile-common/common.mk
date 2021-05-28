# Be silent per default, but 'make V=1' will show all compiler calls.
ifneq ($(V),1)
Q := @
endif

CUR_DIR = $(shell pwd)
TCHAIN ?=
CC      = $(TCHAIN)gcc
CXX     = $(TCHAIN)g++
AS      = $(TCHAIN)gcc
LD      = $(TCHAIN)g++
OBJCOPY = $(TCHAIN)objcopy
AR      = $(TCHAIN)ar
SIZE    = $(TCHAIN)size
OBJDUMP = $(TCHAIN)objdump

# Object files to include
USR_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(USR_SRCS:.c=.o)))
CPP_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(CPP_SRCS:.cpp=.o)))
ASM_OBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(ASM_SRCS:.s=.o)))

# Dependency files to include
DEPS := $(foreach o,$(USR_OBJS),$(o:.o=.d))
DEPS += $(foreach o,$(CPP_OBJS),$(o:.o=.d))

# List files to include
LISTS := $(foreach o,$(USR_OBJS),$(o:.o=.list))
LISTS += $(foreach o,$(CPP_OBJS),$(o:.o=.list))

DEVICE += -ffunction-sections -fdata-sections

INCLUDE_DIRS = -I $(PRJDIR) -I $(SRCDIR) $(addprefix -I, $(USR_INCS))
COMPILE_OPTS = $(DEVICE) -fno-strict-aliasing -fno-common -fomit-frame-pointer -Wall -O$(OPT)

ifeq (${USE_DEBUG},yes)
	COMPILE_OPTS += -g
endif

# Compiler flags to generate listing files:
ifeq (${USE_LIST_OUTPUT},yes)
	COMPILE_OPTS += -Wa,-adhlns=$(@:.o=.list)
endif

# Compiler flags to generate dependency files:
COMPILE_OPTS += -MMD -MP -MF $(@:.o=.d)

# shared lib compiler flags:
ifeq ($(TEMPLATE), sharedlib)
	COMPILE_OPTS += -fPIC
endif

LIBRARY_DIRS = $(USR_LIBS)
PREDEFINES   = $(USR_DEFS)

CFLAGS   += $(COMPILE_OPTS) $(INCLUDE_DIRS) $(PREDEFINES)
CXXFLAGS += $(COMPILE_OPTS) $(INCLUDE_DIRS) $(PREDEFINES)
ASFLAGS  += $(DEVICE) -x assembler-with-cpp -c
LDFLAGS  += $(DEVICE)
LDFLAGS  += -Wl,--gc-sections,-Map=$(PROJECT).map,-cref \
		   $(INCLUDE_DIRS)
ARFLAGS = cr

LIBRARY_LDFLAGS = -shared -Wl,-soname,$@

ifeq (${USE_STATIC_BUILD},yes)
	LDFLAGS += -static
endif

# pkg-config packages depends on
ifneq ($(pkg_packages),)
	PKG_CONFIG := PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:${SYSROOT}/lib/pkgconfig pkg-config
	CFLAGS     += $(shell ${PKG_CONFIG} --cflags $(pkg_packages))
	CXXFLAGS   += $(shell ${PKG_CONFIG} --cflags $(pkg_packages))
	LDFLAGS    += $(shell ${PKG_CONFIG} --libs   $(pkg_packages))
endif

# sysroot for cross compile
ifneq ($(SYSROOT),)
    SYSROOT_FLAG = --sysroot=$(SYSROOT)
    CFLAGS     += $(SYSROOT_FLAG)
    CXXFLAGS   += $(SYSROOT_FLAG)
    LDFLAGS    += $(SYSROOT_FLAG)
endif

# target files
TARGET_MAP    = $(PROJECT).map
TARGET_LIST   = $(PROJECT).list
TARGET_PREFIX =
TARGET_SUBFIX =

# default template type
TEMPLATE ?= app

# app subfix
ifeq ($(TEMPLATE), app)
ifeq ($(OS), Windows_NT)
	TARGET_SUBFIX = .exe
endif
endif

# library prefix and subfix
ifeq ($(TEMPLATE), sharedlib)
ifeq ($(OS), Windows_NT)
	TARGET_SUBFIX = .dll
else
	TARGET_PREFIX = lib
	TARGET_SUBFIX = .so
endif
else ifeq ($(TEMPLATE), staticlib)
	TARGET_PREFIX = lib
	TARGET_SUBFIX = .a
endif

# target name
TARGET = $(TARGET_PREFIX)$(PROJECT)$(TARGET_SUBFIX)

STR_DIV	= ------------------------------------------------------------

# all
all: start $(TARGET) size end

# misc
start:
	@echo Start Compiling Project $(PROJECT)
	@mkdir -p $(OBJ_DIR)

end:
	@echo $(STR_DIV)
	@echo bye!!

gcc-info:
	@echo $(STR_DIV)
	@echo gcc version is
	@$(CC) --version
	@echo $(STR_DIV)

# target
$(TARGET): $(ASM_OBJS) $(USR_OBJS) $(CPP_OBJS)
ifeq ($(TEMPLATE), app)
	@echo "  LD      $(@F)"
	$(Q)$(LD) $(ASM_OBJS) $(USR_OBJS) $(CPP_OBJS) $(LIBRARY_DIRS) $(LDFLAGS) --output $@
else ifeq ($(TEMPLATE), sharedlib)
	@echo "  LD      $(@F)"
	$(Q)$(LD) $(LIBRARY_LDFLAGS) $(ASM_OBJS) $(USR_OBJS) $(CPP_OBJS) --output $@
else ifeq ($(TEMPLATE), staticlib)
	@echo "  AR      $(@F)"
	$(Q)$(AR) $(ARFLAGS) $@ $(ASM_OBJS) $(USR_OBJS) $(CPP_OBJS)
else
	$(error unknown TEMPLATE)
endif

size: $(TARGET)
	@echo $(STR_DIV)
	$(Q)$(SIZE) $(TARGET)

%.list: %.elf
	@echo "  OBJDUMP $@"
	$(Q)$(OBJDUMP) -S $< > $@

$(OBJ_DIR)/%.o: %.s
	@echo "  AS      $(<F)"
	$(Q)$(CC) $(ASFLAGS) -o $@ -c $<

$(OBJ_DIR)/%.o: %.c
	@echo "  CC      $(<F)"
	$(Q)$(CC) $(CFLAGS) -o $@ -c $<

$(OBJ_DIR)/%.o: %.cpp
	@echo "  CXX     $(<F)"
	$(Q)$(CXX) $(CXXFLAGS) -o $@ -c $<

clean:
	@echo "  CLEAN OK!    "
	@-rm -rf $(DEPS) $(USR_OBJS) $(CPP_OBJS) $(TARGET_MAP) $(ASM_OBJS) $(TARGET) $(LISTS) $(TARGET_LIST) $(OBJ_DIR) *.list

install:
ifeq ($(TEMPLATE), app)
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(TARGET) $(DESTDIR)$(PREFIX)/bin
else
	install -d $(DESTDIR)$(PREFIX)/lib
	install -m 755 $(TARGET) $(DESTDIR)$(PREFIX)/lib
endif

# include dependencies
-include $(DEPS)
