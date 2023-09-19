all-upload-test: test build pypi-upload-test clean-dist
pypi-upload-test:
	python3 -m twine upload --repository testpypi dist/*

all-upload-prod: test build pypi-upload-prod clean-dist
pypi-upload-prod:
	python3 -m twine upload dist/* && \
	rm -rf dist

build:
	python3 -m pip install --upgrade build twine && \
	python3 -m build && \
	cd src && \
	ls | grep .egg-info | xargs rm -r
venv:
	python3 -m venv venv
install-pytest: venv
	source venv/bin/activate && \
	pip install pytest
test:
	python3 -m pytest
clean-dist:
	rm -rf dist
