#!/bin/bash


if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
fi

PORT="${PORT:-6789}"

uvicorn main:app --host 0.0.0.0 --port "$PORT" --workers 4
