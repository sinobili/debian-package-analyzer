import pytest

from package_statistics import InvalidArchitectureError, validate_architecture


# --- Test validate_architecture ---
def test_validate_architecture_valid() -> None:
    assert validate_architecture("amd64") == "amd64"
    assert validate_architecture("arm64") == "arm64"


def test_validate_architecture_invalid() -> None:
    with pytest.raises(InvalidArchitectureError):
        validate_architecture("riscv9000")

    with pytest.raises(InvalidArchitectureError):
        validate_architecture("")
