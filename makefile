# Test and linting Makefile
# This Makefile is used to run tests, linting, and type checking for the project.
test:
	PYTHONPATH=. pytest tests

lint:
	flake8 . --exclude venv

format:
	black . --exclude venv

check-types:
	mypy --strict .

run:
	python package_statistics.py amd64

run-json:
	python package_statistics.py amd64 --top 10 --format json

run-verbose:
	python package_statistics.py amd64 --verbose

run-quiet:
	python package_statistics.py amd64 --quiet

docker-run:
	docker-compose up --build
