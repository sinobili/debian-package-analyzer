import logging
import tempfile
import urllib.request
from pathlib import Path

DEBIAN_BASE_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"


class DownloadError(Exception):
    """Custom exception for download-related errors."""

    pass


def get_contents_url(arch: str) -> str:
    """
    Construct the URL to download the Contents-<arch>.gz file.

    Args:
        arch: architecture string (e.g. amd64, arm64)

    Returns:
        Fully qualified URL string
    """
    return f"{DEBIAN_BASE_URL}Contents-{arch}.gz"


def download_contents_file(arch: str) -> Path:
    """
    Downloads the Contents-<arch>.gz file to a temporary file.

    Args:
        arch: Debian architecture (e.g. amd64)

    Returns:
        Path to the downloaded gzip file

    Raises:
        DownloadError: if any error occurs during download
    """
    url = get_contents_url(arch)
    logging.info(f"Downloading contents file from: {url}")

    try:
        # Set timeout to avoid hanging requests
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status != 200:
                raise DownloadError(f"Failed to download: "
                                    f"HTTP {response.status}")

            # Write response to a temporary .gz file on disk
            with tempfile.NamedTemporaryFile(delete=False,
                                             suffix=".gz") as tmp_file:
                tmp_file.write(response.read())
                logging.info(f"File downloaded to: {tmp_file.name}")
                return Path(tmp_file.name)

    except Exception as e:
        # Wrap any exception into a DownloadError
        raise DownloadError(f"Error downloading file: {e}") from e
