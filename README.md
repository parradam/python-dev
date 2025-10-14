# Python dev container

Aims:

- Use a standard, maintained Docker image for Python
- Allow installation of packages using `uv` *after* build
- Decouple development environment from source code

## Building

`docker build -t python-dev .`

## Running

`docker run -it -p 8000:8000 python-dev`

Or start it via Docker/VS Code.

Note: if running FastAPI with uvicorn, don't forgot to pass `--host 0.0.0.0` to access it outside of the container.

## Inside the container

Add packages offline:

`uv add --no-index --find-links=/usr/packages seaborn`

With `uv sync`:

`uv sync --no-index --find-links=/usr/packages`

## Updating dependencies

Update and then copy `python_requirements_raw.txt` into a separate directory and run:

`uv add -r python_requirements_raw.txt`
`uv lock`

This will resolve dependencies as part of the install.

## Exporting as python_requirements.txt

`uv export -f requirements > python_requirements.txt`
