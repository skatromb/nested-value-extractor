# FROM python:3.12 as builder

# RUN curl -sSL https://install.python-poetry.org | python3 -

# ENV POETRY_NO_INTERACTION=1
# ENV POETRY_VIRTUALENVS_IN_PROJECT=1
# ENV POETRY_VIRTUALENVS_CREATE=1
# ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# WORKDIR /app

# COPY pyproject.toml poetry.lock ./
# RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# FROM python:3.11-slim-buster as runtime

# ENV VIRTUAL_ENV=/app/.venv \
#     PATH="/app/.venv/bin:$PATH"

# COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# COPY annapurna ./annapurna

# ENTRYPOINT ["python", "-m", "annapurna.main"]


FROM python:3.12
ARG USER=app
ARG HOMEDIR=/usr/${USER}
RUN useradd --shell /bin/bash --home-dir ${HOMEDIR} --groups sudo ${USER}
USER ${USER}
WORKDIR ${HOMEDIR}

RUN curl --silent --location https://install.python-poetry.org | python3 -
ENV PATH $PATH:${HOMEDIR}/.local/bin
COPY ./ ./
# RUN make all-setup
