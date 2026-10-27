FROM ghcr.io/astral-sh/uv:latest AS uv
FROM python:3.13-slim
COPY --from=uv /uv /uvx /bin/
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY setup.py init_db.py ./
COPY app ./app
CMD ["python", "/app/init_db.py"]
