import urllib.error
from pathlib import Path
from unittest import mock

import pytest

from fetcher import DownloadError, download_contents_file, get_contents_url


# --- Test get_contents_url ---
def test_get_contents_url() -> None:
    arch = "amd64"
    expected_url = (
        "http://ftp.uk.debian.org/debian/dists/stable/main/"
        "Contents-amd64.gz"
    )
    assert get_contents_url(arch) == expected_url


# --- Test download_contents_file with invalid URL (mocked) ---
def test_download_contents_file_failure() -> None:
    with mock.patch(
        "urllib.request.urlopen",
        side_effect=urllib.error.URLError("Mocked error")
    ):
        with pytest.raises(DownloadError) as exc_info:
            download_contents_file("amd64")
        assert "Mocked error" in str(exc_info.value)


# --- Test download_contents_file with successful mock ---
def test_download_contents_file_success() -> None:
    mock_data = b"dummy gzip content"
    mock_response = mock.MagicMock()
    mock_response.__enter__.return_value.status = 200
    mock_response.__enter__.return_value.read.return_value = mock_data

    # For the temp file to have a path with .gz suffix
    temp_path = Path("/tmp/fakefile.gz")

    mock_temp = mock.MagicMock()
    mock_temp.name = str(temp_path)
    mock_temp.__enter__.return_value = mock_temp  # for context manager mock

    with mock.patch("urllib.request.urlopen", return_value=mock_response):
        with mock.patch("tempfile.NamedTemporaryFile", return_value=mock_temp):
            path = download_contents_file("amd64")
            assert path == temp_path
