#
# ifeq ($(TRAVIS_OS_NAME),windows)
# 	SHELL := cmd
# else
# 	SHELL := /bin/bash
# endif

SHELL := /bin/bash

VERSION=$(shell python3 -c "import pyonelab; print(pyonelab.__version__)")

ONELAB_VERSION = "stable"

default:
	@echo "\"make save\"?"

tag:
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

pipy: setup.py
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	rm -f dist/*
	rm -rf pytheas/tools/bin
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal
	twine upload dist/*


gh:
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Pushing to github..."
	git add -A
	@read -p "Enter commit message: " MSG; \
	git commit -a -m "$$MSG"
	git push

publish: tag pipy

test:
	pytest ./tests -s --cov=./

clean: rmonelab rmtmp
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	@rm -rf pytheas_pip.egg-info/ build/ dist/ tmp/
	#cd docs && make clean


lstmp:
	@find . -type d -name 'tmp*'


rmtmp:
	@find . -type d -name 'tmp*' | xargs rm -rf


lsonelab:
	@find . -type f -name '*.pos' -o -name '*.pre' -o -name '*.msh' -o -name '*.res'

rmonelab:
	@find . -type f -name '*.pos' -o -name '*.pre' -o -name '*.msh' -o -name '*.res' | xargs rm -f

lint:
	flake8 setup.py pytheas/ tests/*.py

style:
	@echo "Styling..."
	black setup.py pytheas/ tests/*.py

onelab-linux:
	bash .ci/install_onelab_prebuilt.sh linux $(PWD)/pyonelab/bin/Linux $(ONELAB_VERSION)

onelab-osx:
	bash .ci/install_onelab_prebuilt.sh osx $(PWD)/pyonelab/bin/Darwin $(ONELAB_VERSION)

onelab-windows:
	bash .ci/install_onelab_prebuilt.sh windows $(PWD)/pyonelab/bin/Windows $(ONELAB_VERSION)

onelab: onelab-linux onelab-osx onelab-windows

pyinstall:
	bash .ci/pyinstall.sh

post:
	bash .ci/post.sh

save: clean style gh
