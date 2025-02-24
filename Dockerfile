FROM python:3.13-slim-bookworm

# uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

ENV PYTHONPATH="${PYTHONPATH}:/app/telellm/telellm"

CMD ["echo", "Specify an entrypoint (producer or consumer)"]
