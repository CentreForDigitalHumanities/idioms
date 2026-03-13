FROM docker.io/library/python:3.14-slim AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

FROM python-base AS db-build

COPY scripts/create-db.py ./scripts/create-db.py
COPY data/csv ./data/csv
COPY data/conversion/sql-create-tables.sql ./data/conversion/sql-create-tables.sql
COPY data/conversion/sql-create-fts.sql ./data/conversion/sql-create-fts.sql

RUN python scripts/create-db.py

FROM python-base AS base

COPY requirements.txt requirements-prod.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=db-build --chown=app:app /app/idioms.db ./idioms.db
COPY --chown=app:app metadata.json ./
COPY --chown=app:app plugins ./plugins
COPY --chown=app:app static ./static
COPY --chown=app:app templates ./templates
RUN chown app:app /app

USER app

EXPOSE 8001

FROM base AS local

CMD exec datasette serve . \
    --host 0.0.0.0 \
    --port 8001

FROM base AS prod

USER root

RUN pip install --no-cache-dir -r requirements-prod.txt

# https://docs.datasette.io/en/stable/performance.html#using-datasette-inspect
RUN datasette inspect idioms.db --inspect-file inspect-data.json

USER app

CMD exec datasette gunicorn \
    --immutable idioms.db \
    --inspect-file inspect-data.json \
    --host 0.0.0.0 \
    --port 8001 \
    --workers 4 \
    --metadata metadata.json \
    --template-dir templates \
    --plugins-dir plugins \
    --static static:static \
    --setting default_cache_ttl 60
