PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: help install install-dev install-figures install-data validate test figures dataset-aggregates hf-validate lean

help:
	@echo "Targets:"
	@echo "  make install             Install the package"
	@echo "  make install-dev         Install package plus test/lint deps"
	@echo "  make install-figures     Install figure-regeneration deps"
	@echo "  make install-data        Install dataset-download deps"
	@echo "  make validate            Run syntax, metadata, and numerical checks"
	@echo "  make test                Run pytest tests"
	@echo "  make figures             Regenerate selected public figures"
	@echo "  make dataset-aggregates  Download aggregate JSONs from Hugging Face"
	@echo "  make hf-validate         Check live Hugging Face dataset metadata"
	@echo "  make lean                Build Lean diagnostic checks"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev]"

install-figures:
	$(PIP) install -e ".[figures]"

install-data:
	$(PIP) install -e ".[data]"

validate:
	$(PYTHON) -m py_compile grokking_diag/*.py scripts/*.py
	$(PYTHON) scripts/verify_numerical_claims.py --skip-gpu
	$(PYTHON) -m grokking_diag.cli info

test:
	$(PYTHON) -m pytest -q tests

figures:
	PYTHON=$(PYTHON) bash scripts/regenerate_figures.sh

dataset-aggregates:
	$(PYTHON) scripts/download_dataset.py --cohort aggregates

hf-validate:
	$(PYTHON) scripts/validate_hf_dataset.py

lean:
	cd lean_proofs && lake build Diagnostics
