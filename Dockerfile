FROM python:3.12-slim

ENV PATH="/home/devuser/.local/bin:$PATH"
WORKDIR /usr/src

COPY python_requirements.txt /usr/requirements/python_requirements.txt

# System deps (build tools, Rust for pydantic-core/orjson)
RUN apt-get update && apt-get install -y \
    git nano curl build-essential rustc cargo && \
    rm -rf /var/lib/apt/lists/*

# Create directories before chown
RUN mkdir -p /usr/packages /usr/src/test_project && \
    useradd -ms /bin/bash devuser && \
    chown -R devuser:devuser /usr/src /usr/packages

USER devuser
WORKDIR /usr/src

# Base tools installed for devuser
RUN python -m pip install --user --upgrade pip setuptools wheel pipx maturin \
    && python -m pipx ensurepath \
    && pipx install uv

# Build and cache wheels (ensures maturin/puccinialin dependencies resolved)
RUN mkdir -p /usr/packages && \
    python -m pip wheel --no-cache-dir --wheel-dir /usr/packages -r /usr/requirements/python_requirements.txt

# Create test project and install from local cache
RUN cd /usr/src/test_project && \
    uv init && \
    uv venv && \
    ./.venv/bin/python -m ensurepip && \
    ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
    ./.venv/bin/python -m pip install --no-index --find-links=/usr/packages -r /usr/requirements/python_requirements.txt

# Ensure PATH in bash for devuser
SHELL ["/bin/bash", "-c"]
ENV PATH="/home/devuser/.local/bin:/usr/src/test_project/.venv/bin:$PATH"

EXPOSE 8000
WORKDIR /usr/src
CMD ["bash"]
