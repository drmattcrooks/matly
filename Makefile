#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = mattsplotlib
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif


#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up python interpreter environment and install/update dependencies
create_environment: venv/bin/activate requirements;


## Install or update packages based on requirements.txt
requirements: venv/bin/activate requirements.txt
	. venv/bin/activate; \
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt; \
    $(PYTHON_INTERPRETER) -m ipykernel install --user --name=$(PROJECT_NAME)
	@echo "Requirements up to date & kernal available in notebook as $(PROJECT_NAME) - restart kernel for changes to take effect"
    @echo ">>> virtualenv created/updated. Activate with: \n(mac) source venv/bin/activate \n(Windows) venv\Scripts\activate"
	touch requirements.txt

#### Install Python Dependencies (not in virtualenv)
venv/bin/activate:
	# Create venv folder if doesn't exist. Run make clean to start over.
	test -d venv || $(PYTHON_INTERPRETER) -m venv venv
	. venv/bin/activate; \
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel ipykernel
	@echo ">>> virtualenv created/updated. Activate with: \n(mac) source venv/bin/activate \n(Windows) venv\Scripts\activate"
	touch venv/bin/activate

## Delete all compiled Python files and virtualenv
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	#find . -type d -name "*.egg-info" -exec rm -rf {} \;
	rm -rf dist/
	rm -rf venv/
	rm -rf wheelhouse/

## Run tests
test: create_environment
	. venv/bin/activate; \
	pytest -s --cov=src/ test/ --cov-report term-missing -v