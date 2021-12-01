
# Script is located near this makefile, need to
# do fancy stuff to make that work.
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
HERE := $(notdir $(patsubst %/,%,$(dir $(MKFIKE_PATH))))

ifeq "" "$(HERE)"
HERE:=.
endif

ifndef MOCK_EXE
MOCK_EXE := a.mock.out
endif

ifndef MOCK_SOURCE
$(error MOCK_SOURCE Must be defined, and should include a list of directories to search for source files)
endif

ifndef MOCK_INCLUDE
$(error MOCK_INCLUDE Must be defined, and should include a list of directories to include for headers)
endif

ifndef MOCK_OUTPUT
$(error MOCK_OUTPUT Must be defined, which will hold the built objects, source.mk file, and final exe)
endif

OD := $(shell mkdir -p $(MOCK_OUTPUT))
MOCK_OBJECTS := $(shell python \
          $(HERE)/scripts/source_mk.py \
          "$(MOCK_SOURCE)" \
          "$(MOCK_INCLUDE)" \
          $(MOCK_OUTPUT)/source.mk \
          "$(MOCK_PATCH)")

.PHONY: mock_run mock_build mock_clean test

mock_run: mock_build
	$(info Running Mock '$(MOCK_EXE)')
	$(info ------------)
	@$(MOCK_OUTPUT)/$(MOCK_EXE)

mock_build: $(MOCK_OUTPUT)/$(MOCK_EXE)

include $(MOCK_OUTPUT)/source.mk

${MOCK_OUTPUT}/$(MOCK_EXE): $(FIND_OBJS)
	$(CC) $(FIND_OBJS) -o $(MOCK_OUTPUT)/$(MOCK_EXE) $(FIND_INCLUDES)

mock_clean:
	rm -rf $(MOCK_OUTPUT)
