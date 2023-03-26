FROM python:3.10.10-alpine3.17

ENV PYTHONBUFFERED=1 POETRY_VERSION=1.3.2

EXPOSE 8000

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

CMD python manage.py migrate && \
    python manage.py createprimarytaxon && \
    python manage.py runserver 0.0.0.0:8000