FROM docker.io/library/python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app idioms.db metadata.json ./
COPY --chown=app:app plugins ./plugins
COPY --chown=app:app static ./static
COPY --chown=app:app templates ./templates

USER app

EXPOSE 8001

CMD ["datasette", "gunicorn", "--immutable", "idioms.db", "--host", "0.0.0.0", "--port", "8001", "--workers", "4", "--metadata", "metadata.json", "--template-dir", "templates", "--plugins-dir", "plugins", "--static", "static:static"]
