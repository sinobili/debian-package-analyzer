import gzip
import io
from unittest import mock
import fetcher
import parser
from pathlib import Path


def test_fetch_and_parse_integration(tmp_path: Path) -> None:

    # Simulated contents of a .gz file
    raw_content = (
        "/usr/bin/tool1 pkg1\n"
        "/usr/bin/tool2 pkg2\n"
        "/usr/share/doc/pkg1 README pkg1\n"
        "/usr/lib/libsomething.so pkg2\n"
        "/etc/config.cfg pkg3\n"
        "/etc/config2.cfg pkg3\n"
    )

    # Compress into a .gz in memory
    compressed_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed_buffer, mode="wb") as gz:
        gz.write(raw_content.encode("utf-8"))

    compressed_buffer.seek(0)

    # Create a temporary fake .gz file on disk
    fake_gz_path = tmp_path / "fake.gz"
    fake_gz_path.write_bytes(compressed_buffer.read())

    # Patch the fetcher to return this fake path
    with mock.patch("fetcher.download_contents_file",
                    return_value=fake_gz_path):
        path = fetcher.download_contents_file("amd64")
        result = parser.count_packages(path).most_common()

    # order based on first occurrence in Counter
    assert len(result) == 3
    assert result[0][1] == 2
    assert result[1][1] == 2
    assert result[2][1] == 2
    assert sorted([pkg for pkg, _ in result]) == ["pkg1", "pkg2", "pkg3"]
