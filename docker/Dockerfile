############################## Development stage ##############################

FROM python:3.10-slim-bullseye as development

############### Install poetry ###############

ENV \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry" \
    \
    # Here goes our code. Added to make it importable
    PYTHONPATH="/app"

# Add poetry to path to use the "poetry" command
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    && rm -rf /var/lib/apt/lists/*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Since we're in a container, no need to use venvs
RUN poetry config virtualenvs.create false

############### Install dependencies ###############

# For development
WORKDIR /build
COPY pyproject.toml poetry.lock* ./

# # For production
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

############### Finish up build ###############

# WORKDIR /app
# EXPOSE 3000
# CMD ["python", "manage.py", "start-reload"]


############################## Production stage ##############################

FROM python:3.10-slim-bullseye

# Here goes our code. Added to make it importable
ENV PYTHONPATH="/app"

# Update and install required dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -U pip

COPY --from=development /build/requirements.txt .
RUN pip install -r requirements.txt

COPY src app

EXPOSE 3000

CMD ["python3", "app/users_crud/app.py"]
