uvicorn main:app --reload
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

uv pip install

uv venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows


uv pip install -r requirements.txt 


or use uv sync  (uv sync will read both pyproject.toml and uv.lock if available.)
uv pip list (like pip freeze)