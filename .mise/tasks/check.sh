#!/usr/bin/env bash
#MISE description="Lint/Type check with ruff and ty"
ruff check src/
ty check src/