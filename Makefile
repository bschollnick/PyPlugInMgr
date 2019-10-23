# tag:
	# git tag ${TAG} -m "${MSG}"
	# git push --tags

# venv:
	# virtualenv $@

#requirements: venv requirements.txt
#	. venv/bin/activate; pip install --upgrade -r requirements.txt

#upgrade: requirements
#	. venv/bin/activate; pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

dist:
	del dist /q
	python setup.py sdist bdist_wheel

ptest: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish-test: dist
	twine upload -r pypitest dist/*


publish: dist
	twine upload -r pypi dist/*

#test: requirements
#	. venv/bin/activate; tox

#coverage: test
#	. venv/bin/activate; coverage report

#docs: requirements
#	. venv/bin/activate; cd docs; make html
#	open docs/_build/html/index.html

#.PHONY: dist docs
