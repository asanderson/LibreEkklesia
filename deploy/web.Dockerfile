# The web image: Django under Gunicorn, and the task worker (docs/stack-decisions.md, section 7).
# Build from the repository root: docker build --file deploy/web.Dockerfile .
# Base images are pinned by digest and were at least 7 days old when chosen (section 2).

FROM python:3.13.18-slim-trixie@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# uv builds the virtual environment from backend/uv.lock and stays out of the final image.
FROM base AS build
COPY deploy/requirements-uv.txt /tmp/requirements-uv.txt
RUN pip install --no-cache-dir --require-hashes --requirement /tmp/requirements-uv.txt
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --locked --no-dev

FROM base AS runtime
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app --no-create-home \
        --shell /usr/sbin/nologin app \
    && mkdir -p /data/media /data/site \
    && chown -R app:app /data
COPY --from=build /app/.venv /app/.venv
COPY backend/manage.py ./
COPY backend/config ./config
COPY backend/core ./core
COPY deploy/gunicorn.conf.py ./
COPY deploy/web-healthcheck.py ./healthcheck.py
COPY --chmod=0555 deploy/web-start.sh ./start.sh
ENV PATH=/app/.venv/bin:$PATH \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    LIBREEKKLESIA_DATA_DIR=/data
USER app
EXPOSE 8000
CMD ["./start.sh"]

# The backend tests, run inside the image so they use its Python and SQLite:
# docker build --file deploy/web.Dockerfile --target test .
FROM build AS test-environment
RUN uv sync --locked

FROM runtime AS test
COPY --from=test-environment /app/.venv /app/.venv
COPY backend/pyproject.toml ./
COPY backend/tests ./tests
COPY frontend/src/api/openapi.json /frontend/src/api/openapi.json
ENV DJANGO_SETTINGS_MODULE=config.settings.test \
    LIBREEKKLESIA_DATA_DIR=/tmp/libreekklesia-test
RUN python -m pytest -p no:cacheprovider
