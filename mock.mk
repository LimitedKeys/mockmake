
HERE := $(CURDIR)

ifndef MOCK_SOURCE
$(error MOCK_SOURCE Must be defined)
endif

ifndef MOCK_INCLUDE
$(error MOCK_INCLUDE Must be defined)
endif

ifndef MOCK_OUTPUT
$(error MOCK_OUTPUT Must be defined)
endif

OD := $(shell mkdir -p $(MOCK_OUTPUT))
MOCK_OBJECTS := $(shell python \
          $(HERE)/scripts/find_mk.py \
          $(MOCK_SOURCE) \
          $(MOCK_OUTPUT) \
          source.mk)

.PHONY: mock_run mock_build mock_clean test

mock_run: mock_build
	$(info Running Mock)
	$(info ------------)
	@$(MOCK_OUTPUT)/a.out

mock_build: $(MOCK_OUTPUT)/a.out

include $(MOCK_OUTPUT)/source.mk

$(MOCK_OUTPUT)/a.out: $(FIND_OBJS)
	$(CC) $(FIND_OBJS) -o \
		$(MOCK_OUTPUT)/a.out

mock_clean:
	rm -rf $(MOCK_OUTPUT)
