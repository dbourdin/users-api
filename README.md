# Users API
This project holds a Users REST API


## Requirements
**Make sure you have the following installed before you proceed**
* Python 3 - [Install Python 3](https://www.python.org/downloads/)
* Docker - [Install Docker](https://hub.docker.com/search/?type=edition&offering=community)
* docker-compose - [Install docker-compose](https://docs.docker.com/compose/install/)

## Develop locally
First, make sure you're working in a virtual environment, and run:
```bash
$ ./scripts/configure.sh
```
This sets up git hooks to run on every commit and install required local python
dependencies.


### Using Docker
You can develop the API locally by running it in a Docker container. To do so,
you'll have to run it with start_develop.sh:
```bash
$ ./scripts/start_develop.sh
```
This will run the API and all the required services within Docker containers.

Then go to http://127.0.0.1:3000/docs to see the Swagger UI.


### Without Docker
First you'll have to set up the project and it's dependencies. You will need to
[install Poetry](https://python-poetry.org/docs/).

After installing Poetry, install all project dependencies with:
```bash
$ poetry install
```

You have to set some environment variables first:
```bash
$ export POSTGRES_SERVER=127.0.0.1
$ export POSTGRES_USER=posgres
$ export POSTGRES_PASSWORD=postgres
$ export POSTGRES_DB=users
$ export SECRET_KEY=secret
```

Now you can run the API using an ASGI service like
[Uvicorn](https://www.uvicorn.org/)
```bash
$ uvicorn users_api.app:app
```

There is a convenience "django-like" CLI that helps you do common operations,
located in `src/users_api/cli/manage.py`. You can start the API with:
```bash
$ python manage.py start-reload
```

Then go to http://127.0.0.1:3000/docs to see the Swagger UI.

**NOTE:** By running the app without Docker, you'll have to set up a database
and apply migrations. You can apply migrations using:
```bash
$ python manage.py migrate
```

## API Configuration
The configuration file is `config/api.env`. Its contents are sent to the
container and parsed by the config loader. If you want to change a value,
edit the file and then run `./scripts/start_develop.sh` again, so that Docker
respawns the container with the updated environment.

## DB Configuration
The configuration file is `config/db.env`. Its contents are sent to the
container and parsed by the config loader. If you want to change a value,
edit the file and then run `./scripts/start_develop.sh` again, so that Docker
respawns the container with the updated environment.

## Unit tests
Tests are defined in the `tests` folder. You can run the whole suite in an
ephemeral container with:
```bash
$ ./scripts/test.sh
```
