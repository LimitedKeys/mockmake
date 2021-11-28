
.PHONY: test clean all

all: test

test:
	python -m pytest tests

clean:
	rm -rf __pycache__
	rm -rf output
