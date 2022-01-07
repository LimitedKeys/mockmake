
VERSION := 1.0.0
ARCHIVE := mockmake-${VERSION}.zip

.PHONY: test clean all save

all: test

test:
	python -m pytest tests

clean:
	rm -rf __pycache__
	rm -rf output

save: ${ARCHIVE}

$(ARCHIVE):
	git archive -o ./archive/$(ARCHIVE) HEAD
