#!/bin/sh
set -e

MODEL=${OLLAMA_MODEL:-qwen3:8b}

until ollama list >/dev/null 2>&1; do
    echo "Waiting for Ollama..."
    sleep 2
done

if ollama list | grep -q "$MODEL"; then
    echo "Model $MODEL already exists"
else
    echo "Pulling $MODEL..."
    ollama pull "$MODEL"
fi