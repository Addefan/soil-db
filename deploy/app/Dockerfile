FROM python:3.10.10

ENV PYTHONBUFFERED=1 POETRY_VERSION=1.3.2 PORT=8000

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

RUN python manage.py collectstatic --noinput


CMD python manage.py createprimarytaxon && \
    uwsgi --ini deploy/app/uwsgi.ini --http-socket :$PORT --static-map /static=/app/static