init:
	@pip install -r requirements.txt

test:
	@rm -f .coverage
	@./run_tests.sh

upload:
	@python setup.py sdist upload -r pypi
