# Sane Makefile configuration -------------------------------------------------

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c  
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# If a Make rule fails, it’s target file is deleted. This ensures the next
# time you run Make, it’ll properly re-run the failed rule, and guards against
# broken files.
.DELETE_ON_ERROR:

ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

# -----------------------------------------------------------------------------

DC=docker-compose

down:
> $(DC) stop
.PHONY: down

up:
> $(DC) up -d
.PHONY: up

logs:
> $(DC) logs -f
.PHONY: logs

rm:
> $(DC) rm -f
.PHONY: rm

build:
> $(DC) build
.PHONY: build


server-sh:
> echo $(shell hostname)
> $(DC) exec server /bin/bash
.PHONY: server-sh

worker-sh:
> echo $(shell hostname)
> $(DC) exec worker /bin/bash
.PHONY: worker-sh

ipy:
> $(DC) run --rm server ipython
.PHONY: ipy

node-sh:
> $(DC) run --rm node /bin/bash
.PHONY: node-sh

# Since make doesn't do argument forwarding, use this like 
#
#   $ PKG=some-package-name make node-add-pkg`
#
node-add-pkg:
> $(DC) exec webpack yarn add $$PKG
.PHONY: node-add-pkg

test:
> $(DC) run --rm server pytest
.PHONY: test

restart: down rm up logs
.PHONY: restart
