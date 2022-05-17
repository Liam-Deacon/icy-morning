TF_EXEC ?= terraform
SERVERLESS_EXEC ?= serverless
APP ?= icy-morning

PYTHON_VERSION ?= $(shell cat ../.python-version | echo 3.9.9)
PYTHON_MAJOR_MIN = $(shell echo $(PYTHON_VERSION) | sed 's/-dev//' | cut -d '.' -f1,2)
PIP_COMMAND ?= eval "$$(pyenv init -)" && pyenv shell $(PYTHON_VERSION) && python3 -m pip

.PHONY: \
	create-infrastructure \
	destroy-infrastructure \
	init \
	lint \
	test \
	terraform_deploy \
	terraform_destroy \
	serverless_deploy \
	serverless_destroy 

init:
	$(TF_EXEC) init

clean:
	rm -rf ../dist ../build/tmp/

create-archive: icy-morning-fast-api.zip

$(APP)-fast-api.zip:
	rm -rf ../build/tmp ../dist && \
	mkdir -p ../build/tmp ../dist && \
	find ../app | grep -E "__pycache__$$" | xargs rm -rf && \
	cp -rf ../app ../build/tmp/ && \
	$(PIP_COMMAND) install -r ../requirements.txt --target ../build/tmp && \
	cd ../build/tmp && zip -r ../../dist/$(APP)-fast-api.zip . && \
	rm -rf ../build/tmp

fmt:
	$(TF_EXEC) fmt

lint:
	$(TF_EXEC) fmt -check -recursive -diff

test:
	$(SERVERLESS_EXEC) invoke -f $(APP)

terraform_deploy: create-archive
	$(TF_EXEC) apply

terraform_destroy:
	$(TF_EXEC) destroy -var=\"stage=dev\"

serverless_deploy:
	$(SERVERLESS_EXEC) deploy -f $(APP) --stage dev

serverless_destroy:
	$(SERVERLESS_EXEC) remove --stage dev

deploy: terraform_deploy serverless_deploy

destroy: serverless_destroy terraform_destroy

create-infrastructure: deploy

destroy-infrastructure: destroy

.ONESHELL:
main.tf:
	@bash generate_backend_config.sh