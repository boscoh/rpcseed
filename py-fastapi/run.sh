PORT="8000"
./browser.sh "http://localhost:$PORT" &
uv run uvicorn main:app --reload --port="$PORT"
