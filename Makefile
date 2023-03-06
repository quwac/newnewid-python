.PHONY: test
test:
	PYTHONPATH=./src poetry run pytest -s --cache-clear tests

.PHONY: publish
publish:
	bash scripts/publish.sh .env
