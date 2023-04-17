.PHONY: test
test:
	PYTHONPATH=./src poetry run pytest -s --cache-clear --html=report.html --self-contained-html tests

.PHONY: publish
publish:
	bash scripts/publish.sh .env
