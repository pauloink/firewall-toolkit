#!/usr/bin/env python3

import argparse
import csv
import socket
from pathlib import Path


DEFAULT_TIMEOUT = 5


def load_targets(file_path):
    targets = []

    with file_path.open(encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

        for line_number, row in enumerate(reader, start=1):
            if not row or row[0].strip().startswith("#"):
                continue

            if len(row) != 2:
                raise ValueError(
                    f"Invalid entry on line {line_number}: "
                    "expected hostname,port"
                )

            hostname = row[0].strip()

            try:
                port = int(row[1].strip())
            except ValueError as error:
                raise ValueError(
                    f"Invalid port on line {line_number}"
                ) from error

            if not 1 <= port <= 65535:
                raise ValueError(
                    f"Port out of range on line {line_number}"
                )

            targets.append((hostname, port))

    if not targets:
        raise ValueError("No valid targets were found")

    return targets


def check_connection(hostname, port, timeout):
    try:
        with socket.create_connection(
            (hostname, port),
            timeout=timeout,
        ):
            return "OPEN"

    except socket.timeout:
        return "TIMEOUT — check firewall, routing or service availability"

    except ConnectionRefusedError:
        return "REFUSED — destination reachable but service rejected connection"

    except socket.gaierror:
        return "DNS ERROR — hostname could not be resolved"

    except OSError as error:
        return f"FAILED — {error}"


def save_results(results, output_file):
    with output_file.open("w", encoding="utf-8", newline="\n") as file:
        for hostname, port, status in results:
            file.write(f"{hostname}:{port}\t{status}\n")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Test TCP connectivity to multiple destinations "
            "defined in a CSV file."
        )
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("targets.csv"),
        help="Input CSV file (default: targets.csv)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("results.txt"),
        help="Output file (default: results.txt)",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Connection timeout in seconds (default: 5)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.timeout <= 0:
        raise ValueError("Timeout must be greater than zero")

    targets = load_targets(args.input)
    results = []

    print(f"Testing {len(targets)} destination(s)...")

    for hostname, port in targets:
        status = check_connection(
            hostname,
            port,
            args.timeout,
        )

        results.append((hostname, port, status))
        print(f"{hostname}:{port} — {status}")

    save_results(results, args.output)

    print(f"\nResults saved to: {args.output.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        raise SystemExit(f"Error: {error}")
