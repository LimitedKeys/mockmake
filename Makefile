
VERSION := 1.3.0
ARCHIVE := mockmake-${VERSION}.zip

.PHONY: test clean all save

all: test

test:
	python -m pytest tests

clean:
	rm -rf __pycache__
	rm -rf output

save: archive/${ARCHIVE}

archive/$(ARCHIVE):
	git archive -o ./archive/$(ARCHIVE) HEAD
