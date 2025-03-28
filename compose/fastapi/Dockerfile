FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN apt-get update -y \
  && apt-get install gcc -y

WORKDIR /src

RUN pip install poetry

COPY poetry.lock pyproject.toml /src/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY ./src /src
