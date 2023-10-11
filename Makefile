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

gen-doc:
	(cd docs && rm -f generated/*.rst ; PYTHONPATH=.. sphinx-autogen ../pygamelib/*.py ../pygamelib/*/*.py ../pygamelib/*/*/*.py  -o ./generated)
	@echo ""
	@echo "GENERATED DOC WAS WRITTEN IN docs/generated PLEASE HAVE A LOOK AT IT AND IMPORT THE DOC YOU NEED MANUALLY BY MOVING THE RELEVANT FILES TO docs/source"

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