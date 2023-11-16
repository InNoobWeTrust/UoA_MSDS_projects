# Ref: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
# The builder image, used to build the virtual environment
FROM python:3.10-buster as builder

RUN pip install --no-cache-dir poetry==1.5.0

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.10-slim-buster as runtime

LABEL name="Ad Recommender Flask"
LABEL reference="https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0"
LABEL description="The code is part of Capstone project 1 \
    for MSc in Data Science at University of Arizona"

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY data/ /app/data
COPY templates/ /app/templates
COPY app.py /app/app.py

WORKDIR /app
EXPOSE 80

ENTRYPOINT [".venv/bin/python3", "-m", "gunicorn", "-b", "0.0.0.0:80", "app:app"]
