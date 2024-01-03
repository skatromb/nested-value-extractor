test:
	$(with_venv) && python3 -m pytest

all-upload-test: test build pypi-upload-test clean-dist

all-upload-prod: test build pypi-upload-prod clean-dist

all-setup: venv pre-commit-install install-deps

with_venv := . .venv/bin/activate
set-env:
	export PATH=$PATH:.venv/bin/
venv: clean-venv
	python3.12 -m venv .venv
pypi-upload-test:
	$(with_venv) && \
	python3 -m twine upload --repository testpypi dist/*
pypi-upload-prod:
	$(with_venv) && \
	python3 -m twine upload dist/*
pre-commit-install:
	pip install pre-commit && pre-commit install-hooks
install-deps: venv
	$(with_venv) && \
	pip install -r requirements.dev.txt
build:
	$(with_venv) && \
	pip install --upgrade build twine && \
	python -m build && \
	cd src && \
	ls | grep .egg-info | xargs rm -r
poetry:
	curl -sSL https://install.python-poetry.org | python3 -
clean-dist:
	rm -rf dist
clean-venv:
	rm -rf .venv
