# tap-flowcode

`tap-flowcode` is a Singer tap for Flowcode.

## Installation

```bash
pipx install tap-flowcode
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-flowcode --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

This tap uses OAuth and apikey as authentication methods, provide a client id, client secret and a refresh token in the config file for OAuth and an apikey for apikey authentication.

## Usage

You can easily run `tap-flowcode` by itself.

### Executing the Tap Directly

```bash
tap-flowcode --version
tap-flowcode --help
tap-flowcode --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_flowcode/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-flowcode` CLI interface directly using `poetry run`:

```bash
poetry run tap-flowcode --help
```
