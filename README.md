# Python dev container

Aims:

- Use a standard, maintained Docker image for Python
- Allow installation of packages using `uv` *after* build
- Decouple development environment from source code

## Building

Win11: 
`. ./build.ps1`

Linux:
`docker build -t python-dev .`

## Running

`docker run -it -p 8000:8000 python-dev`

Or start it via Docker/VS Code.

Note: if running FastAPI, don't forgot to pass `--host 0.0.0.0` to access it outside of the container.
