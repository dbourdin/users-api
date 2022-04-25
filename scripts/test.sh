#!/bin/bash

# Runs the test suite inside a container


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
docker-compose -f "$SCRIPT_DIR"/../docker/docker-compose.yml \
 run \
 --rm \
 users-api \
 pytest --cov="users_api" $@

docker-compose -f "$SCRIPT_DIR"/../docker/docker-compose.yml down
