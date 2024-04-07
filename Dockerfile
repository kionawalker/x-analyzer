# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-buster

ENV POETRY_VERSION=1.8 \
    POETRY_VIRTUALENVS_CREATE=false

# Basic tools
RUN apt update && apt-get update
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt install -y build-essential libbz2-dev libdb-dev \
    libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
    libncursesw5-dev libsqlite3-dev libssl-dev \
    zlib1g-dev uuid-dev tk-dev

RUN apt install -y nano curl wget git man

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR ${WORKDIR}
# COPY poetry.lock pyproject.toml /home/workspace/
COPY ./* ${WORKDIR}

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

ENTRYPOINT [ "tail", "-F", "/dev/null" ]
