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

Build the local or production image with Podman or Docker (substitute `podman` with `docker`):

```sh
# Local
podman build --target local -t idioms:local -f Containerfile .
# Production
podman build --target prod -t idioms:prod -f Containerfile .
```

Run the app:

```sh
podman run --rm -p 8001:8001 idioms:local
```

The app will be available at <http://127.0.0.1:8001/>.

## License

The data are licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
The source code is licensed under the [3-Clause BSD License](https://opensource.org/license/bsd-3-clause/).
See the `LICENSE` file for details.
