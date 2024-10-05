FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/src

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends gcc


COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
  && poetry install $(test "$WORK_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-cache

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY src .
