FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev

COPY . /app

ARG GOOGLE_APPLICATION_CREDENTIALS=/app/google/mide-lo-que-importa-279017-74408be1c57e.json
ARG SQLALCHEMY_DATABASE_URL=sqlite:///./celes.db
ARG SECRET_KEY=3cd55ae03539bf078a0be5f56794d3d76804b4e09ef276e5d47de85e75b474b5
ARG ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV GOOGLE_APPLICATION_CREDENTIALS ${GOOGLE_APPLICATION_CREDENTIALS}
ENV SQLALCHEMY_DATABASE_URL  ${SQLALCHEMY_DATABASE_URL}
ENV SECRET_KEY  ${SECRET_KEY}
ENV ACCESS_TOKEN_EXPIRE_MINUTES  ${ACCESS_TOKEN_EXPIRE_MINUTES}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
