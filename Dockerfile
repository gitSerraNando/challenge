FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app


ENV ACCESS_TOKEN_EXPIRE_MINUTES  ${ACCESS_TOKEN_EXPIRE_MINUTES}
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
