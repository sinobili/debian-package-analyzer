import argparse
import json
import logging
import sys
import time
from parser import ParseError, count_packages
from fetcher import DownloadError, download_contents_file

# --- Configure Logging ---
# Default logging config (can be overridden by --verbose/--quiet)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --- Valid Architectures ---
# Set of officially supported Debian architectures
VALID_ARCHITECTURES = {
    "amd64",
    "arm64",
    "armhf",
    "i386",
    "mips",
    "mipsel",
    "ppc64el",
    "s390x",
}


class InvalidArchitectureError(Exception):
    """Custom exception for unsupported architectures."""
    pass


def validate_architecture(arch: str) -> str:
    """Validate if the given architecture is supported."""
    if arch not in VALID_ARCHITECTURES:
        raise InvalidArchitectureError(
            f"Unsupported architecture: '{arch}'. Supported values are: "
            f"{', '.join(sorted(VALID_ARCHITECTURES))}"
        )
    return arch


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Fetch and analyze Debian Contents index "
            "for a given architecture."
        )
    )
    parser.add_argument(
        "arch",
        type=validate_architecture,
        help="CPU architecture (e.g. amd64, arm64, i386)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top packages to display (default: 10)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: text or json (default: text)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug output",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational logs",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI tool."""
    contents_path = None  # Temp path to downloaded file
    try:
        start = time.perf_counter()  # Start timing
        args = parse_args()

        # Configure log level based on user flags
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        elif args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        else:
            logging.getLogger().setLevel(logging.INFO)

        logging.info(f"Architecture selected: {args.arch}")
        logging.info(f"Top N packages to display: {args.top}")

        # Download .gz contents file
        contents_path = download_contents_file(args.arch)
        logging.info(f"Contents file saved at: {contents_path}")

        # Parse and count packages
        package_counts = count_packages(contents_path)
        top_packages = package_counts.most_common(args.top)

        # Output results
        if args.format == "json":
            print(json.dumps(top_packages, indent=2))  # Pretty print as JSON
        else:
            print(f"\nTop {args.top} packages by number of files:\n")
            for name, count in top_packages:
                print(f"{name:<30} {count}")  # Text format aligned

        # Print time taken for the operation
        duration = time.perf_counter() - start
        logging.info(f"Completed in {duration:.2f} seconds.")

    except InvalidArchitectureError as e:
        logging.error(str(e))
        sys.exit(1)
    except DownloadError as e:
        logging.error(f"Download failed: {e}")
        sys.exit(2)
    except ParseError as e:
        logging.error(f"Parsing failed: {e}")
        sys.exit(3)
    except Exception:
        logging.exception("Unexpected error occurred.")
        sys.exit(99)
    finally:
        # Cleanup downloaded file if it exists
        if contents_path and contents_path.exists():
            try:
                contents_path.unlink()
                logging.info(f"Temporary file {contents_path} deleted.")
            except Exception as cleanup_error:
                logging.warning(f"Failed to delete "
                                f"temporary file: {cleanup_error}")


if __name__ == "__main__":
    main()
