FROM python:3.13

# Upgrade system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Ensure UV installs from /usr/packages, not from PyPI
# ENV UV_INDEX_URL=file:///usr/packages
# ENV UV_NO_INDEX=1

ENV PATH="/home/devuser/.local/bin:$PATH"
WORKDIR /usr/src

COPY python_requirements_pinned_hashless.txt /usr/requirements/python_requirements_pinned_hashless.txt
# COPY pyproject.toml /usr/requirements/pyproject.toml
COPY template /usr/src/template
COPY fastapi-starter /usr/src/fastapi-starter

# System deps (build tools, Rust for pydantic-core/orjson)
RUN apt-get update && apt-get install -y \
    python3-venv python3-pip git nano curl build-essential rustc cargo && \
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
RUN python -m pip wheel --no-cache-dir --wheel-dir=/usr/packages -r /usr/requirements/python_requirements_pinned_hashless.txt

# Create test project and install from local cache
RUN cd /usr/src/template && \
    uv venv --clear && \
    ./.venv/bin/python -m ensurepip && \
    ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
    uv add --no-index --find-links=/usr/packages --requirements /usr/requirements/python_requirements_pinned_hashless.txt

# fastapi-starter
RUN mkdir -p /usr/src/fastapi-starter/requirements

RUN cd /usr/src/fastapi-starter && \
    uv export -f requirements > fastapi-requirements.txt && \
    python -m pip wheel --no-cache-dir --wheel-dir=/usr/packages -r fastapi-requirements.txt

RUN cd /usr/src/fastapi-starter && \
    uv venv --clear && \
    ./.venv/bin/python -m  ensurepip && \
    ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
    uv sync --no-index --find-links=/usr/packages

# # Build and cache wheels for fastapi-starter using uv.lock
# RUN cd /usr/src/fastapi-starter && \
#     uv export -f requirements > fastapi-requirements.txt && \
#     python -m pip wheel --no-cache-dir --wheel-dir=/usr/packages -r fastapi-requirements.txt

# # Install fastapi-starter from local cache
# RUN cd /usr/src/fastapi-starter && \
#     uv venv --clear && \
#     ./.venv/bin/python -m ensurepip && \
#     ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
#     uv sync --no-index --find-links=/usr/packages


# # Build and cache wheels for fastapi-starter
# RUN cd /usr/src/fastapi-starter && \
#     uv export --output-file /tmp/fastapi-requirements.txt && \
#     python -m pip wheel --no-cache-dir --wheel-dir=/usr/packages -r /tmp/fastapi-requirements.txt

# # fastapi-starter
# RUN cd /usr/src/fastapi-starter && \
#     uv venv && \
#     ./.venv/bin/python -m ensurepip && \
#     ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
#     uv sync --no-index --find-links=/usr/packages

# Create fastapi-starter project and install from local cache
# RUN cd /usr/src/fastapi-starter && \
#     uv venv && \
#     ./.venv/bin/python -m ensurepip && \
#     ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
#     uv add --no-index --find-links=/usr/packages --requirements /usr/requirements/python_requirements_pinned_hashless.txt

# RUN cd /usr/src/fastapi-starter && \
#     uv venv --clear && \
#     ./.venv/bin/python -m ensurepip && \
#     ./.venv/bin/python -m pip install --upgrade pip setuptools wheel && \
#     uv sync --no-index --find-links=/usr/packages || true && \
#     # build wheels for all installed packages into /usr/packages
#     ./.venv/bin/python -m pip wheel --wheel-dir=/usr/packages -r <(./.venv/bin/python -m pip freeze)

# Ensure UV installs from /usr/packages, not from PyPI
ENV UV_INDEX_URL=file:///usr/packages
ENV UV_NO_INDEX=1

# Ensure PATH in bash for devuser
SHELL ["/bin/bash", "-c"]
ENV PATH="/home/devuser/.local/bin:/usr/src/template/.venv/bin:$PATH"

EXPOSE 8000
WORKDIR /usr/src
CMD ["bash"]
