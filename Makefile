init:
	@pip install -r requirements.txt

test:
	@rm -f .coverage
	@./run_tests.sh
