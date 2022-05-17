
PYTHON_VERSION ?= $(shell cat .python-version | echo 3.8.13)
PYTHON_MAJOR_MIN = $(shell echo $(PYTHON_VERSION) | sed 's/-dev//' | cut -d '.' -f1,2)
AWS_ACCOUNT_ID ?= account_id
AWS_REGION ?= eu-west-2
AWS_ECR ?= $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
VENV_COMMAND ?= bash .venv/bin/activate &&


all: init docker-build

docker-login:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ECR)

docker-build:
	docker build -t $(AWS_ECR)/fastapi-aws-lambda:latest . -f aws_lambda.dockerfile

docker-push:
	docker push -t $(AWS_ECR)/fastapi-aws-lambda:latest

.PHONY: init
init: venv pyenv

.PHONY: pyenv
pyenv:
	which pyenv || bash pyenv-install.sh

serverless:
	which serverless || (nvm install 16; nvm use 16 && npm install -g serverless) 

clean:
	rm -rf venv
	rm -f db.sqlite

.venv:
	pyenv install --skip-existing $(PYTHON_VERSION) && pyenv local $(PYTHON_VERSION) | true
	(python$(PYTHON_VERSION) -m venv .venv || python$(PYTHON_MAJOR_MIN) -m venv .venv || \
	 eval "$$(pyenv init -)" && pyenv shell $(PYTHON_VERSION) && python3 -m venv .venv) && \
	$(VENV_COMMAND) python -m pip install --upgrade pip && \
	$(VENV_COMMAND) python -m pip install setuptools wheel && \
	$(VENV_COMMAND) python -m pip install -r requirements.txt

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
	pylint app
	
.PHONY: serve
serve:
	uvicorn app.api.main_app:app --reload

.PHONY: test
test:
	$(VENV_COMMAND) BASIC_AUTH_USERNAME=sonic BASIC_AUTH_PASSWORD=robotnik python -m pytest -s -vv tests
