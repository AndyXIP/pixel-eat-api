run:
	@uv run uvicorn main:app --reload --app-dir src

check:
	@ruff check . && ty check .

fix:
	@ruff check . --fix && ruff format .
