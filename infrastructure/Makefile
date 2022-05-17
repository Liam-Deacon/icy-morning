TF_EXEC ?= terraform
SERVERLESS_EXEC ?= serverless
APP ?= icy-morning

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
	rm -rf ../dist ../tmp

create-archive: icy-morning-fast-api.zip

icy-morning-fast-api.zip:
	rm -rf ../tmp ../dist
	mkdir -p ../tmp ../dist
	cp -rf ../app/*  ./tmp/
	pip3 install -r ./requirements.txt --target ../tmp
	cd ../tmp && zip -r ../dist/$(APP)-fast-api.zip .
	rm -rf ../tmp

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