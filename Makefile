
PYTHON_VERSION ?= 3.10.4

all: init

.PHONY: init
init: venv pyenv

.PHONY: pyenv
pyenv:
	which pyenv || bash pyenv-install.sh

.PHONY: peotry
poetry:
	which poetry

clean:
	rm -rf venv

venv:
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install setuptools wheel
	venv/bin/python -m pip install -r requirements.txt

start:
	uvicorn main:app --reload