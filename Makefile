# /************************************************************************
# Name: Lukas (Viridis) Dubsik
# Login: xdubsil00
# Project: IRCOMP
# School-Project: ITU-1
# ************************************************************************/

PYTHON ?= python3

.PHONY: install install-dev build run check format pack

install:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
	npm --prefix web ci

install-dev: install
	.venv/bin/python -m pip install -r requirements-dev.txt

build:
	npm --prefix web run build

run:
	.venv/bin/ircomp-gui

check:
	.venv/bin/ruff check src
	.venv/bin/ruff format --check src
	.venv/bin/pyright
	npm --prefix web run check

format:
	.venv/bin/ruff format src
	npm --prefix web run format

pack:
	git diff --quiet HEAD
	test -z "$$(git ls-files --others --exclude-standard)"
	mkdir -p submission
	git archive --format=zip --prefix=IRCOMP-GUI/ --output=submission/00_xdubsil00_source.zip HEAD
	cd submission && sha256sum 00_xdubsil00_source.zip > 00_xdubsil00_source.zip.sha256
