
PYTHON_VERSION ?= 3.10.4

all: init

.PHONY: init
init: venv pyenv

.PHONY: pyenv
pyenv:
	which pyenv || bash pyenv-install.sh

.PHONY: poetry
poetry:
	which poetry

clean:
	rm -rf venv
	rm db.sqlite

venv:
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	venv/bin/python -m pip install --upgrade pip
	venv/bin/python -m pip install setuptools wheel
	venv/bin/python -m pip install -r requirements.txt

.PHONY: fmt
fmt:
	black . $(ARGS)

.PHONY: install
install:
	pip3 install --user --requirement requirements.txt

.PHONY: install-dev
install-dev:
	pip3 install --user --requirement requirements-dev.txt	

.PHONY: lint
lint:
	pylint *.py
	
.PHONY: serve
serve:
	uvicorn main:app --reload

.PHONY: test
test:
	python -m pytest -s -vv tests

.PHONY: zip
zip:
	pip3 install --target ./libs --requirement requirements.txt
	cd ./libs && zip -rq ../lambda.zip .
	zip -gq lambda.zip main.py
	mv lambda.zip ../infra/modules/api-gateway
	rm -r ./libs
