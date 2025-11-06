FROM python:3.13-slim

# System deps for building wheels and Python packages
RUN apt-get update && apt-get install -y \
    python3-venv python3-pip build-essential rustc cargo git curl nano && \
    rm -rf /var/lib/apt/lists/*

# Paths and working dir
ENV PATH="/home/devuser/.local/bin:$PATH"
WORKDIR /usr/templates

# Create user and directories
RUN useradd -ms /bin/bash devuser && \
    mkdir -p /usr/packages /usr/templates/fastapi-starter /usr/requirements && \
    chown -R devuser:devuser /usr/src /usr/packages /usr/requirements

COPY fastapi-starter /usr/templates/fastapi-starter

USER root
RUN chown -R devuser:devuser /usr/templates
RUN chown -R devuser:devuser /usr/src
USER devuser

WORKDIR /usr/templates/fastapi-starter

# Install pipx and uv
RUN python -m pip install --user --upgrade pip setuptools wheel pipx && \
    python -m pipx ensurepath && \
    pipx install uv

# Initialize uv project and venv
RUN uv venv --clear && \
    ./.venv/bin/python -m ensurepip --upgrade && \
    ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
    uv sync

# Expose FastAPI port
EXPOSE 8000
WORKDIR /usr/src
CMD ["bash"]
