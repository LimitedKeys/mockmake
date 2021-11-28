
MOCK_SOURCE += ./src
MOCK_INCLUDE += ./src
MOCK_OUTPUT = ./output

OD := $(shell mkdir -p $(MOCK_OUTPUT))
HERE := $(shell pwd)
MOCK_OBJECTS := $(shell python \
          $(HERE)/scripts/find_mk.py \
          $(MOCK_SOURCE) \
          $(MOCK_OUTPUT) \
          source.mk)

.PHONY: all clean

all: $(MOCK_OUTPUT)/a.out

include $(MOCK_OUTPUT)/source.mk

$(MOCK_OUTPUT)/a.out: $(FIND_OBJS)
	$(CC) $(FIND_OBJS) -o \
		$(MOCK_OUTPUT)/a.out

clean:
	rm -rf output
