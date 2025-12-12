FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y \
    build-essential curl ca-certificates software-properties-common \
    git ffmpeg && rm -rf /var/lib/apt/lists/*

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_DEV=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

RUN uv pip install -U streamlit

USER nonroot

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
