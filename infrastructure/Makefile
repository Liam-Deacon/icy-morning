TF_EXEC ?= terraform
SERVERLESS_EXEC ?= serverless
APP ?= icy-morning

PYTHON_VERSION ?= $(shell cat ../.python-version | echo 3.8.13)
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
	rm -f api_gateway_custom_domain.tf

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

check:
	$(TF_EXEC) init 1>/dev/null 2>/dev/null
	$(TF_EXEC) plan -var basic_auth_password=changeme -var basic_auth_username=testuser

test: init
	checkov --framework terraform -d .

api_gateway_custom_domain.tf:
	cp ./templates/api_gateway_custom_domain.tf.tpl api_gateway_custom_domain.tf

terraform_init:
	$(TF_EXEC) init

terraform_deploy: create-archive
	$(TF_EXEC) apply

terraform_destroy:
	$(TF_EXEC) destroy -var=\"stage=dev\"

serverless_deploy:
	$(SERVERLESS_EXEC) deploy -f $(APP) --stage dev

serverless_destroy:
	$(SERVERLESS_EXEC) remove --stage dev

deploy: terraform_init terraform_deploy #serverless_deploy

destroy:
	@true || $(MAKE) serverless_destroy
	$(MAKE) terraform_destroy

create-infrastructure: deploy

destroy-infrastructure: destroy

.ONESHELL:
main.tf:
	@bash generate_backend_config.sh