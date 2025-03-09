[![CI Python](https://github.com/miem-refugees/telellm/actions/workflows/ci.yml/badge.svg)](https://github.com/miem-refugees/telellm/actions/workflows/ci.yml)
[![Docker](https://github.com/miem-refugees/telellm/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/miem-refugees/telellm/actions/workflows/docker-publish.yml)

# Telegram bot for LLM interaction

## Overview

This repository contains a Telegram bot that can be used to interact with LLMs.

## Usage

To use the bot, you need to create a Telegram bot and obtain its API token. You can then
use the bot by sending it a message in the chat.

## Dependencies

The following libraries are required:

* Python 3.x
* `ruff` library for linting
* `pytest` library for testing

## Installation

To install the bot, run the following command:

```bash
uv sync
```

## Running the bot

Application is splitted with redis queue and db. The incoming user message put into task
queue by bot and consumed by server. The result can be get with command `/status <uuid>`.

Run the bot (producer):

```bash
python telellm/main.py
```

Run server (consumer):

```bash
python telellm/consumer.py
```

You can also run both using Docker:

```bash
docker-compose up -d
```

## Testing

To run the tests, use the following command:

```bash
pytest
```

## Linting

To lint the code, use the following command:

```bash
ruff telellm
```

## Kubernetes deployment

1. Secrets:
```bash
kubectl apply -f secrets-config.yaml
```

2. Redis and Ollama:
```bash
kubectl apply -f redis-deployment.yaml
kubectl apply -f ollama-deployment.yaml
```

3. ConfigMap, bot and consumer:
```bash
kubectl apply -f configmap.yaml
kubectl apply -f bot-deployment.yaml
kubectl apply -f consumer-deployment.yaml
```

4. Ingress:
```bash
kubectl apply -f ingress.yaml
```

5. Ollama init job:
```bash
kubectl apply -f ollama-init-job.yaml
```

6. Ollama model update cronjob:
```bash
kubectl apply -f model-update-cron.yaml
```
