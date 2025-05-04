import gzip
import logging
from collections import Counter
from typing import Counter as CounterType  # clearer alias
from pathlib import Path
from typing import Iterator


from tqdm import tqdm  # For progress bar on large files


class ParseError(Exception):
    """Custom exception for parse-related errors."""

    pass


def stream_contents_file(path: Path) -> Iterator[str]:
    """
    Yields lines from a gzip-compressed Contents file, one at a time.

    Args:
        path: Path to .gz file

    Yields:
        Lines as strings (without newline)
    """
    try:
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                yield line.strip()
    except OSError as e:
        raise ParseError(f"Failed to open gzip file: {e}") from e


def count_packages(path: Path) -> CounterType[str]:
    """
    Parses the Contents file and returns a counter of package name ->
    number of files.

    Args:
        path: Path to .gz file

    Returns:
        Counter mapping package name -> file count
    """
    logging.info("Parsing contents file...")
    counter: Counter[str] = Counter()

    # Wrap streaming with tqdm to show progress bar
    for line in tqdm(stream_contents_file(path), desc="Parsing", unit="line"):
        if not line or " " not in line:
            continue  # Skip malformed or empty lines

        try:
            # Safely split at last whitespace, even if path contains spaces
            parts = line.rsplit(maxsplit=1)
            packages = parts[1] if len(parts) == 2 else ""
            for pkg in packages.split(","):
                counter[pkg] += 1
        except Exception as e:
            logging.warning(f"Skipping malformed line: {line} - {e}")
            continue

    logging.info(f"Parsed {len(counter)} unique packages.")
    return counter
