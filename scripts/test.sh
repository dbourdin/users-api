#!/bin/bash

# Runs the test suite inside a container

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Ensure all containers are down
docker-compose -f "$SCRIPT_DIR"/../docker/docker-compose.yml down

# Run tests
docker-compose -f "$SCRIPT_DIR"/../docker/docker-compose.yml \
 run \
 --rm \
 users-api \
 pytest --cov="users_api" $@

# Tear down environment
docker-compose -f "$SCRIPT_DIR"/../docker/docker-compose.yml down
