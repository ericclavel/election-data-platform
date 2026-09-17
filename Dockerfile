FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.12.13 /uv /uvx /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY ingestion/ingest_data.py ./ingest_data.py
ENTRYPOINT ["python", "ingest_data.py"]