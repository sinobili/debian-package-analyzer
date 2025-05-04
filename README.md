# Debian Package File Statistics Tool

## Overview
This command-line tool downloads and parses the Debian "Contents" index file for a given CPU architecture. It extracts and displays the top N packages with the most files associated with them.

The project was developed as part of a technical assessment for a Junior Software Developer - Observability role. The code prioritizes modularity, testability, error handling, and observability.

---

## Key Features

- Modular structure with separate modules for downloading, parsing, and CLI orchestration
- Robust error handling with custom exceptions and exit codes
- Type-safe code using Python's type hints and `mypy` strict mode
- Inline progress bar using `tqdm`
- Logging support with `--verbose` and `--quiet` flags
- Support for `json` or `text` output formats
- Fully tested with unit and integration tests
- Docker support for containerized execution

---

## Approach to the Task

- **Python Best Practices**: Followed PEP8, added type hints, and used `flake8`, `black`, `mypy --strict`.
- **Modular Design**: Separated downloading (`fetcher.py`), parsing (`parser.py`), and CLI (`package_statistics.py`) to ensure maintainability and testability.
- **Testability**: Wrote 11 unit and integration tests using `pytest`.
- **Observability**: CLI logs key stages with `logging`, and uses a progress bar while parsing large files.
- **Robustness**: Used custom error classes and distinct exit codes for architecture validation, download, and parsing failures.

---

## Project Structure

- `package_statistics.py`: CLI entry point and orchestration logic.
- `fetcher.py`: Downloads the compressed `Contents-<arch>.gz` file.
- `parser.py`: Parses and counts file associations for packages.
- `tests/`: Contains all unit and integration tests.
- `Dockerfile` / `docker-compose.yml`: For reproducible execution.
- `Makefile`: Developer shortcuts for testing, linting, type checking.
- `requirements.txt`: Runtime dependencies.
- `requirements-dev.txt`: Development dependencies for CI and testing.

---

## Quick Start

```bash
python package_statistics.py amd64
```

With optional arguments:

```bash
python package_statistics.py amd64 --top 10 --format json --verbose
```

---

##  Docker Support

```bash
docker-compose up --build
```

or using Makefile:

```bash
make docker-run
```

> Logs and results will appear in the container output.

---

##  Development Workflow

```bash
# Set up environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
make test

# Lint & format
make lint
make format

# Type check
make check-types
```

---

## Example Output

```bash
$ python package_statistics.py amd64 --verbose

2025-05-05 01:16:31 [INFO] Architecture selected: amd64
2025-05-05 01:16:31 [INFO] Top N packages to display: 10
2025-05-05 01:16:31 [INFO] Downloading contents file from: http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz
2025-05-05 01:16:32 [INFO] File downloaded to: /var/folders/...gz
2025-05-05 01:16:32 [INFO] Contents file saved at: /var/folders/...gz
2025-05-05 01:16:32 [INFO] Parsing contents file...
Parsing: 1659104line [00:00, 1935047.41line/s]
2025-05-05 01:16:33 [INFO] Parsed 32341 unique packages.

Top 10 packages by number of files:

devel/piglit                   53007
science/esys-particle          18408
math/acl2-books                16907
libdevel/libboost1.81-dev      15456
libdevel/libboost1.74-dev      14333
lisp/racket                    9599
net/zoneminder                 8161
electronics/horizon-eda        8130
libdevel/libtorch-dev          8089
libdevel/liboce-modeling-dev   7458
2025-05-05 01:16:33 [INFO] Completed in 1.74 seconds.
2025-05-05 01:16:33 [INFO] Temporary file ... deleted.
```

---

## Code Quality Tools

- `flake8` for linting and style compliance
- `black` for consistent formatting
- `mypy` for static type checks
- `pytest` for unit and integration testing

---

##  Design Considerations

###  Observability
- Structured logging using `logging`
- Flags for verbosity
- Timings measured with `time.perf_counter()`

###  Performance
- Streamed file parsing for memory efficiency
- Progress bar (`tqdm`) for large files
- <2s execution on standard architectures

###  Robustness
- Graceful failure and exit codes:
  - `1`: Invalid architecture
  - `2`: Download error
  - `3`: Parse error
  - `99`: Unexpected
- UTF-8 decode error handling

###  Extensibility
- Modular structure: `fetcher.py`, `parser.py`, etc.
- Easily extensible output format (`--format csv`?)
- Streaming model can replace temp file in future

---

##  Testing Strategy

- Unit tests with `pytest`
- Mocks for file downloading and argument parsing
- Integration test across fetcher + parser
- Edge case tests: empty file, invalid arch, decode errors

---

##  Time Spent

**~8 hours total**, including:
- Environment setup
- CLI + downloader + parser implementation
- Testing and observability
- Docker & Make integration
- Cleanup, lint, type checks, and README

---

## Final Notes
The project fulfills all core requirements of the assessment prompt while incorporating extra improvements such as Docker support, detailed error handling, progress reporting, and CI-oriented practices. The code is cleanly organized and designed to be easily extensible.

If this were to evolve into a production tool, the next step would be switching to a stream-based parser using `BytesIO` to handle large files more efficiently without intermediate disk writes.

##  Author

**Sinasi Ibrahim Gurpinar**  

- GitHub: [sinobili](https://github.com/sinobili)
- LinkedIn: [linkedin.com/in/sinasi-ibrahim-gurpinar-68a874136](https://www.linkedin.com/in/sinasi-ibrahim-gurpinar-68a874136/)
