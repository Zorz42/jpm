ifeq (,$(which python))
	PYTHON := python
endif
ifeq (,$(which python3))
	PYTHON := python3
endif

all: fullinstall

fullinstall: install.py
	@$(PYTHON) install.py dependencies
	@$(PYTHON) install.py install
