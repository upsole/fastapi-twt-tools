FROM python:3

ENV POETRY_VERSION 1.1.12

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install 

COPY ./ ./
COPY .env .env

CMD ["poetry", "run", "python", "-m", "api"]
