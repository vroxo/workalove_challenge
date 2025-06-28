# Dockerfile
FROM python:3.13-rc-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . /app

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]