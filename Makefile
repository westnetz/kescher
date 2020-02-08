.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run software tests
	rm -f kescher.log kescher.db
	pytest -v kescher --cov=./ --cov-report term-missing:skip-covered $(PYTEST_ARGS)

.PHONY: black
black: ## Format code
	python -m black kescher

.PHONY: run
run: ## Run kescher and import fixtures
	rm -f kescher.log kescher.db
	kescher init
	@kescher import-journal kescher/tests/fixtures/journal.csv
	@kescher import-accounts kescher/tests/fixtures/accounts.yaml
	@kescher import-documents kescher/tests/fixtures/documents
	@kescher import-invoices kescher/tests/fixtures/invoices_nested cid total_gross date
