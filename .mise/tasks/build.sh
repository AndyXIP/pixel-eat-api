#!/usr/bin/env bash
#MISE description="Build the Docker image"
docker build --build-arg UV_VERSION="$(mise current uv)" -t pixel-eat-api .
