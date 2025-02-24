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
