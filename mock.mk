
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MOCK_ROOT_DIR := $(dir $(MKFILE_PATH))

# Default Executables / Commands that can be over written
ifndef PYTHON
PYTHON := python
endif

ifndef RMDIR
RMDIR := rm -rf
endif

ifndef MKDIR
MKDIR := mkdir -p
endif

# Mock Make stuff

ifndef MOCK_EXE
MOCK_EXE := a.mock.out
endif

ifndef MOCK_SOURCE
$(error MOCK_SOURCE not defined. MOCK_SOURCE must be defined and contain a list of directories to search for C files)
endif

ifndef MOCK_INCLUDE
$(error MOCK_INCLUDE not defined. MOCK_INCLUDE must be defined and contain a list of directories to include while building the C files and linking the executable)
endif

FIND_INCLUDE := $(addprefix -I,$(MOCK_INCLUDE))

ifndef MOCK_OUTPUT
$(error MOCK_OUTPUT not defined. MOCK_OUTPUT must be defined, and set to an outpt directory. This directory will hold the object files, source.mk file, and final exe)
endif

ifdef MOCK_PATCH
ifndef MOCK_PSCRIPT
$(error MOCK_PSCRIPT not defined. MOCK_PSCRIPT must be defined in order to patch files. Please set MOCK_PSCRIPT to the path of the python patch script)
endif
endif

ifdef MOCK_PSCRIPT
ifndef MOCK_PATCH
$(error MOCK_PATCH not defined. MOCK_PATCH must be defined with a list of files to patch with MOCK_PSCRIPT)
endif
endif

# output dir needs made before python script runs
OD := $(shell $(MKDIR) $(MOCK_OUTPUT))

# Define FIND_SRC
MOCK_OBJECTS := $(shell $(PYTHON) \
          $(MOCK_ROOT_DIR)/scripts/source_mk.py \
          "$(MOCK_OUTPUT)/source.mk" \
          "$(MOCK_SOURCE)")
include $(MOCK_OUTPUT)/source.mk

# Add source files to the search path
FIND_SRC_DIRS:=$(dir $(FIND_SRC))
vpath %.c $(FIND_SRC_DIRS)

# Strip the ./ from patch files
#
# the found source files will not have the ./
MOCK_PATCH_FIXED:=$(subst ./,,$(MOCK_PATCH))
MOCK_PATCH_SRC:=$(addprefix $(MOCK_OUTPUT)/, \
    $(notdir $(MOCK_PATCH_FIXED:.c=.patch.c)))
MOCK_PATCH_OBJ:=$(MOCK_PATCH_SRC:.c=.o)

# filter out patch files - patch files will have
# different build procedures
FIND_SRC_NO_PATCH=$(filter-out $(MOCK_PATCH_FIXED),$(FIND_SRC))

# Get a list of .o files
FIND_SRC_FILES:=$(notdir $(FIND_SRC_NO_PATCH))
FIND_SRC_OBJS:=$(addprefix $(MOCK_OUTPUT)/,$(FIND_SRC_FILES:.c=.o))

.PHONY: mock_all mock_run mock_build mock_clean mock_generate

mock_all: mock_build mock_run mock_generate
mock_build: $(MOCK_OUTPUT)/$(MOCK_EXE)

mock_run: mock_build
	$(info Running Mock '$(MOCK_EXE)')
	$(info ------------)
	@$(MOCK_OUTPUT)/$(MOCK_EXE)

# when chaining pattern rules, intermediate 
# files are deleted by defaulit.
#
# patch.c files are deleted by default normally,
# unless you make the recipe depend on them
mock_generate: $(MOCK_PATCH_SRC)

$(MOCK_OUTPUT)/$(MOCK_EXE): $(FIND_SRC_OBJS) $(MOCK_PATCH_OBJ)
	$(MKDIR) $(@D)
	$(CC) $^ -o $@ $(FIND_INCLUDE)

%.patch.o: %.patch.c
	$(MKDIR) $(@D)
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@ $(FIND_INCLUDE)

# main.patch.c: src/main.c $(MOCK_PSCRIPT)
$(MOCK_OUTPUT)/%.patch.c: %.c $(MOCK_PSCRIPT)
	$(MKDIR) $(@D)
	$(PYTHON) $(MOCK_PSCRIPT) $< $@

$(MOCK_OUTPUT)/%.o: %.c
	$(MKDIR) $(@D)
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@ $(FIND_INCLUDE)

mock_clean:
	$(RMDIR) $(MOCK_OUTPUT)

