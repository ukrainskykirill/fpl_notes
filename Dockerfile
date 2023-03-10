FROM python:3.11-slim

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY ./fpl_notes /code/fpl_notes

WORKDIR /code/fpl_notes