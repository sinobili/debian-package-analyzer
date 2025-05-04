import pytest
import sys
from pathlib import Path
from unittest import mock
import package_statistics
from _pytest.monkeypatch import MonkeyPatch
from _pytest.capture import CaptureFixture


def test_main_valid_args(monkeypatch: MonkeyPatch,
                         capsys: CaptureFixture[str]) -> None:
    test_args = ["package_statistics.py", "amd64", "--top", "5"]
    monkeypatch.setattr(sys, "argv", test_args)

    with mock.patch("package_statistics."
                    "download_contents_file") as mock_download, \
         mock.patch("package_statistics.count_packages") as mock_count:

        # Simulate path returned by downloader
        fake_path = Path("/tmp/fake.gz")
        mock_download.return_value = fake_path

        # Mock .most_common() return
        mock_counter = mock.MagicMock()
        mock_counter.most_common.return_value = [
            ("pkg1", 10),
            ("pkg2", 9),
            ("pkg3", 8),
            ("pkg4", 7),
            ("pkg5", 6),
        ]
        mock_count.return_value = mock_counter

        # Call main and capture output
        package_statistics.main()
        captured = capsys.readouterr()
        assert "pkg1" in captured.out
        assert "pkg5" in captured.out


def test_main_invalid_arch(monkeypatch: MonkeyPatch) -> None:
    test_args = ["package_statistics.py", "invalid_arch"]
    monkeypatch.setattr(sys, "argv", test_args)

    with pytest.raises(SystemExit):
        package_statistics.main()
