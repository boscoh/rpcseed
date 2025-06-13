PORT="8000"
uv sync
uv run uvicorn main:app --reload --port="$PORT"
