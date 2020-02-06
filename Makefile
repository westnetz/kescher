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
