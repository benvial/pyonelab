

.PHONY: test clean

SHELL := /bin/bash

VERSION=$(shell python3 -c "import pyonelab; print(pyonelab.__version__)")

ONELAB_VERSION = "stable"

version:
	@echo version $(VERSION)

tag:
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

pipy: setup.py pipbuild
	twine upload dist/*

pipbuild: cleanpreppip
		@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
		rm -rf dist/*
		python3 setup.py sdist
		python3 setup.py bdist_wheel --universal

cleanpreppip:
	rm -rf pyonelab/bin

publish: tag pipy

gh:
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Pushing to github..."
	git add -A
	@read -p "Enter commit message: " MSG; \
	git commit -a -m "$$MSG"
	git push

test:
	pytest ./test --cov=./

clean: rmonelab rmtmp cleanpreppip
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	@rm -rf pyonelab.egg-info/ build/ dist/ tmp/
	rm -rf pyonelab/bin/*


lstmp:
	@find . -type d -name 'tmp*'


rmtmp:
	@find . -type d -name 'tmp*' | xargs rm -rf


lsonelab:
	@find . -type f -name '*.pos' -o -name '*.pre' -o -name '*.msh' -o -name '*.res'

rmonelab:
	@find . -type f -name '*.pos' -o -name '*.pre' -o -name '*.msh' -o -name '*.res' | xargs rm -f

lint:
	flake8 setup.py pyonelab/ test/*.py

style:
	@echo "Styling..."
	black setup.py pyonelab/ test/*.py

onelab-linux:
	python dev/install_onelab_prebuilt.py Linux $(PWD)/pyonelab/bin/Linux $(ONELAB_VERSION)

onelab-osx:
	python dev/install_onelab_prebuilt.py Darwin $(PWD)/pyonelab/bin/Darwin $(ONELAB_VERSION)

onelab-windows:
	python dev/install_onelab_prebuilt.py Windows $(PWD)/pyonelab/bin/Windows $(ONELAB_VERSION)

onelab: onelab-linux onelab-osx onelab-windows

pyinstall:
	bash .ci/pyinstall.sh

post:
	bash .ci/post.sh

save: clean style gh
