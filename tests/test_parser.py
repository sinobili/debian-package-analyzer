import gzip
import tempfile
from collections import Counter
from parser import ParseError, count_packages
from pathlib import Path

import pytest

# Sample small .gz contents data
test_lines = """
bin/bash bash
usr/bin/python3 python3,python3-minimal
usr/bin/ls coreutils
""".strip().split(
    "\n"
)


def create_test_gz_file(lines: list[str]) -> Path:
    """
    Utility function to create a temporary .gz file from provided lines
    """
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".gz")
    with gzip.open(temp.name, "wt", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return Path(temp.name)


def test_count_packages_basic() -> None:
    # Test with a small set of lines
    # Create a temporary gzipped file
    path = create_test_gz_file(test_lines)
    counter = count_packages(path)

    assert isinstance(counter, Counter)
    assert counter["bash"] == 1
    assert counter["python3"] == 1
    assert counter["python3-minimal"] == 1
    assert counter["coreutils"] == 1

    path.unlink()  # Clean up temp file


def test_count_packages_malformed() -> None:
    # Test with some malformed lines
    # Create a temporary gzipped file with some malformed lines
    malformed_lines = ["thislinehasnospaces", "",
                       "usr/bin/something pack1,pack2"]
    path = create_test_gz_file(malformed_lines)
    counter = count_packages(path)
    assert counter["pack1"] == 1
    assert counter["pack2"] == 1
    path.unlink()


def test_count_packages_invalid_file() -> None:
    # Provide non-gz file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        f.write(b"not gzip content")
        fpath = Path(f.name)

    with pytest.raises(ParseError):
        count_packages(fpath)

    fpath.unlink()
