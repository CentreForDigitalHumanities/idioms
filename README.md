# Database of Dutch Dialect Idioms

This repository contains a [Datasette](https://datasette.io/) app for serving the [Database of Dutch Dialect Idioms](https://dutchdialectidioms.uu.nl/). It preserves the data structures of the now-retired original project database, and includes the data in TSV format.

## Installation

Datasette can be installed and run directly using Python, as well as via a Podman/Docker image.

### 1. Local Python install

#### Prerequisites

- Python (v3.10+)

#### Virtual environment

Create and activate your virtual environment:

    python3 -m venv .venv --prompt="(idiomsdb) "
    source .venv/bin/activate

Install base Datasette dependencies:

    pip install -r requirements.txt

Import the data into a SQLite database:

    python scripts/create-db.py

Alternatively, download [idioms.db](https://dutchdialectidioms.uu.nl/idioms.db) and place it in the root directory of the project.

#### Running Datasette

    source .venv/bin/activate
    datasette serve .

### 2. Container image

The repository includes a multi-stage `Containerfile` (compatible with Docker) for building either a local image with the base dependencies from `requirements.txt`, or a production image that adds `requirements-prod.txt`.
During the image build, `scripts/create-db.py` is run against the tracked `data/` sources so `idioms.db` is generated inside the build and baked into the final image.

Build the local image with Podman or Docker (substitute `podman` with `docker`):

```sh
# Local
podman build --target local -t idioms:local -f Containerfile .
```

Run the app:

```sh
podman run --rm -p 8001:8001 idioms:local
```

The app will be available at <http://127.0.0.1:8001/>.

## Development

```sh
# Upgrade dependencies
uv pip compile --universal --upgrade --python-version 3.14 requirements.in --output-file=requirements.txt
uv pip compile --universal --upgrade --python-version 3.14 requirements-prod.in --output-file requirements-prod.txt
# Test the prod image locally:
podman build --target prod -t idioms:prod -f Containerfile .
podman run --rm --name idioms --env-file ./env.prod -p 8001:8001 -u 1000:0 idioms:prod
```

### Release

Before creating a new version tag, bump the app version in `CITATION.cff`.

To update the dataset version, update the following values:
- The `version` field in `metadata.json`.
- The `version` and `date-released` field in `data/CITATION.cff`
- The `version` and `date-released` field of the referenced dataset in the main `CITATION.cff`.

## License

The data are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
The source code is licensed under the [3-Clause BSD License](https://opensource.org/license/bsd-3-clause/).
See the `LICENSE` file for details.
