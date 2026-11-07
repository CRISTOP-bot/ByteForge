PYTHON ?= python3

.PHONY: train test c cpp
train:
	$(PYTHON) src/python/train.py

test:
	$(PYTHON) -m unittest discover -s tests -v

c:
	$(MAKE) -C src/c

cpp:
	$(MAKE) -C src/cpp
