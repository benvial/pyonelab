

SHELL := /bin/bash

# VERSION=$(shell python3 -c "import gyptis; print(gyptis.__version__)")
VERSION=$(shell python3 -c "import pyonelab; print(pyonelab.__version__)")

ONELAB_VERSION = "stable"

default:
	@echo "\"make save\"?"
	echo $(VERSION)

tag:
	# Make sure we're on the master branch
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Tagging v$(VERSION)..."
	git tag v$(VERSION)
	git push --tags

pipy: setup.py pipbuild
	twine upload dist/*

pipbuild: preppip
		@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
		rm -rf dist/*
		python3 setup.py sdist
		python3 setup.py bdist_wheel --universal

preppip: cleanpreppip
	python3 preppip.py

cleanpreppip:
	rm -rf pyonelab-Linux
	rm -rf pyonelab-Darwin
	rm -rf pyonelab-Windows

publish: tag pipy

gh:
	@if [ "$(shell git rev-parse --abbrev-ref HEAD)" != "master" ]; then exit 1; fi
	@echo "Pushing to github..."
	git add -A
	@read -p "Enter commit message: " MSG; \
	git commit -a -m "$$MSG"
	git push



test:
	pytest ./tests -s --cov=./

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
	flake8 setup.py pyonelab/ tests/*.py

style:
	@echo "Styling..."
	black setup.py pyonelab/ tests/*.py

onelab-linux:
	bash docker/install_onelab_prebuilt.sh Linux $(PWD)/pyonelab/bin/Linux $(ONELAB_VERSION)

onelab-osx:
	bash docker/install_onelab_prebuilt.sh Darwin $(PWD)/pyonelab/bin/Darwin $(ONELAB_VERSION)

onelab-windows:
	bash docker/install_onelab_prebuilt.sh Windows $(PWD)/pyonelab/bin/Windows $(ONELAB_VERSION)

onelab: onelab-linux onelab-osx onelab-windows

pyinstall:
	bash .ci/pyinstall.sh

post:
	bash .ci/post.sh

save: clean style gh
