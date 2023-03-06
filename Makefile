
.PHONY: test
test:
	PYTHONPATH=./src poetry run pytest --cache-clear
