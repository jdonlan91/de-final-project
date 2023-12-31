PROJECT_NAME = de-final-project
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD=$(shell pwd)
PYTHONPATH=${WD}
SHELL := /bin/bash
PROFILE = default
PIP:=pip
INGESTOR_UTILS_PATH="$(WD)/src/ingestor"
PROCESSOR_UTILS_PATH="$(WD)/src/processor"
LOADER_UTILS_PATH="$(WD)/src/loader"

create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> check python3 version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

ACTIVATE_ENV := source venv/bin/activate

define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

bandit:
	$(call execute_in_env, $(PIP) install bandit)

safety:
	$(call execute_in_env, $(PIP) install safety)

flake:
	$(call execute_in_env, $(PIP) install flake8)

coverage:
	$(call execute_in_env, $(PIP) install coverage)

dev-setup: bandit safety flake coverage

security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)

	$(call execute_in_env, bandit -lll *c/*/*.py *c/*/utils/*.py)

run-flake:
	$(call execute_in_env, flake8  ./src/*/*.py ./test/*/*.py *c/*/utils/*.py)

unit-test:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}:${INGESTOR_UTILS_PATH}:${PROCESSOR_UTILS_PATH}:${LOADER_UTILS_PATH} pytest -v)

check-coverage:
	$(call execute_in_env, PYTHONPATH=${PYTHONPATH}:${INGESTOR_UTILS_PATH}:${PROCESSOR_UTILS_PATH}:${LOADER_UTILS_PATH} coverage run --omit 'venv/*' -m pytest && coverage report -m)

run-checks: security-test run-flake unit-test check-coverage

package-utils:
	./scripts/package-utils.sh
