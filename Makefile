tpp: test clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pp: test clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

coverage:
	coverage run --source=./pygamelib -m unittest discover -s tests
	coverage report
	coverage html
	coverage xml

test:
	python3 -m unittest discover -s tests

doc:
	cd docs && make html

clean:
	rm -rf dist/
	rm -rf pygamelib.egg-info/
	rm -f .coverage
	find ./ -iname '*.pyc' | xargs rm -f
	find ./ -iname '*.pyo' | xargs rm -f
	find ./ -iname '__pycache__' | xargs rm -rf
	(cd docs && make clean)

devenv:
	pip3 install --user pipenv
	pipenv install --dev

all: coverage doc clean pp

.PHONY: tpp pp test clean doc