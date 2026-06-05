# SPDX-License-Identifier: Apache-2.0
# One-command developer workflow. See CONTRIBUTING.md.
PYTHON  ?= python3
VENV    := .venv
VENV_PY := $(VENV)/bin/python
BUILD   ?= build

.DEFAULT_GOAL := help

.PHONY: help dev test test-py test-c lint fmt bench fuzz docs serve-docs wheel sdist clean

# Apple's clang lacks the libFuzzer runtime; on macOS use Homebrew LLVM:
#   make fuzz FUZZ_CC="$$(brew --prefix llvm)/bin/clang"
FUZZ_CC   ?= clang
FUZZ_TIME ?= 30

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

$(VENV_PY):
	$(PYTHON) -m venv $(VENV)

dev: $(VENV_PY) ## Create venv, install dev deps, build the CFFI extension
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -e ".[dev,docs]"
	@echo "Activate with: source $(VENV)/bin/activate"

test: test-c test-py ## Run C tests and Python tests

test-py: ## Run the Python test suite
	$(VENV_PY) -m pytest

test-c: ## Build and run the C tests via CMake/CTest
	cmake -S . -B $(BUILD) -DADDLIB_BUILD_TESTS=ON
	cmake --build $(BUILD)
	ctest --test-dir $(BUILD) --output-on-failure

C_SOURCES := c/src/*.c c/include/add/*.h c/tests/*.c c/fuzz/*.c c/bench/*.c examples/*.c

lint: ## Lint C and Python (clang-format, ruff, mypy)
	$(VENV_PY) -m ruff check .
	$(VENV_PY) -m ruff format --check .
	$(VENV_PY) -m mypy
	$(VENV)/bin/clang-format --dry-run --Werror $(C_SOURCES)

fmt: ## Auto-format C and Python
	$(VENV_PY) -m ruff format .
	$(VENV_PY) -m ruff check --fix .
	$(VENV)/bin/clang-format -i $(C_SOURCES)

bench: ## Run benchmarks
	$(VENV_PY) -m pytest benchmarks --benchmark-only

fuzz: ## Build & run the libFuzzer target (macOS: FUZZ_CC="$$(brew --prefix llvm)/bin/clang")
	@mkdir -p $(BUILD)
	$(FUZZ_CC) -g -O1 -fsanitize=fuzzer,address,undefined \
		-Ic/include c/src/add.c c/fuzz/fuzz_add.c -o $(BUILD)/fuzz_add
	$(BUILD)/fuzz_add -max_total_time=$(FUZZ_TIME) -print_final_stats=1

docs: ## Build the documentation site
	$(VENV_PY) -m mkdocs build --strict

serve-docs: ## Serve docs locally with live reload
	$(VENV_PY) -m mkdocs serve

wheel: ## Build a wheel for the current platform
	$(VENV_PY) -m build --wheel

sdist: ## Build a source distribution
	$(VENV_PY) -m build --sdist

clean: ## Remove build artifacts
	rm -rf $(BUILD) dist *.egg-info python/src/*.egg-info site .pytest_cache .mypy_cache .ruff_cache
	find . -path ./$(VENV) -prune -o -name '__pycache__' -type d -print | xargs rm -rf
	find python/src/addlib -name '_add_cffi*' -delete
