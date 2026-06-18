# TCP Connectivity Checker

A cross-platform Python utility that tests TCP connectivity to multiple destinations and records the results.

## Status results

- `OPEN`: TCP connection completed successfully
- `REFUSED`: destination responded but rejected the connection
- `TIMEOUT`: no response before the configured timeout
- `DNS ERROR`: hostname could not be resolved
- `FAILED`: another network or operating-system error occurred

A timeout does not prove that a firewall is blocking traffic. Routing problems, packet loss and unavailable systems can produce similar results.

## Requirements

- Python 3.10+
- Network access to the authorized destinations

No external Python packages are required.

## Configuration

Copy the example target list:

### Linux or macOS

```bash
cp targets.example.csv targets.csv
```

### Windows PowerShell

```powershell
Copy-Item targets.example.csv targets.csv
```

Each line must contain a hostname or IP address and a TCP port:

```csv
example.com,443
192.0.2.10,80
```

## Usage

```bash
python connectivity_checker.py
```

Custom input, output and timeout:

```bash
python connectivity_checker.py \
  --input targets.csv \
  --output results.txt \
  --timeout 10
```

Display help:

```bash
python connectivity_checker.py --help
```

## Security

Use this utility only against systems where you have explicit authorization.

Do not publish target files or results containing internal hostnames, IP addresses or infrastructure details.

## Disclaimer

Connection results should be combined with firewall logs, routing information and service monitoring before drawing conclusions.
