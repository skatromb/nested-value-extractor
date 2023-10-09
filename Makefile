test:
	$(with_venv) && python3 -m pytest

all-upload-test: clean-dist test build pypi-upload-test clean-dist

all-upload-prod: clean-dist test build pypi-upload-prod clean-dist

all-setup: venv pre-commit-install install-deps

with_venv := source .venv/bin/activate
venv: clean-venv
	python3.12 -m venv .venv
pypi-upload-test:
	$(with_venv) && \
	python3 -m twine upload --repository testpypi dist/*
pypi-upload-prod:
	$(with_venv) && \
	python3 -m twine upload dist/*
pre-commit-install:
	pre-commit install
install-deps: venv
	$(with_venv) && \
	pip install -r requirements.dev.txt
build:
	$(with_venv) && \
	pip install --upgrade build twine && \
	python -m build && \
	cd src && \
	ls | grep .egg-info | xargs rm -r
clean-dist:
	rm -rf dist
clean-venv:
	rm -rf .venv
