# Cisco ASA Packet-Tracer Checker

A Python utility that connects to a Cisco ASA over SSH and runs the built-in `packet-tracer` command to analyze a simulated TCP or UDP connection.

The tool displays the complete packet-tracer output and identifies whether the simulated traffic was allowed or dropped.

## Features

- Connects securely using SSH
- Supports TCP and UDP simulations
- Validates IP addresses, ports and interface names
- Supports privileged EXEC mode
- Displays the complete packet-tracer analysis
- Shows configured access groups when traffic is dropped
- Does not store credentials

## Requirements

- Python 3.10+
- SSH access to an authorized Cisco ASA
- Valid ASA credentials
- Permission to execute `packet-tracer`
- Knowledge of the traffic ingress interface

## Installation

From the repository root:

```bash
cd cisco-asa
python -m venv .venv
```

Activate the environment and install the dependency:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python asa_rule_checker.py
```

The script requests:

- ASA management address
- Username and password
- Enable secret
- Source IP address and port
- Destination IP address and port
- TCP or UDP protocol
- Traffic ingress interface

Example:

```text
ASA management IP: 192.0.2.10
Username: admin
Source IP: 198.51.100.10
Source port: 3333
Destination IP: 203.0.113.20
Destination port: 443
Protocol (TCP or UDP): tcp
Ingress interface name: inside
```

All addresses above are reserved documentation examples.

## Determining the ingress interface

The ingress interface represents where the simulated source traffic enters the ASA.

You can investigate routing and interface configuration using commands such as:

```text
show route
show nameif
```

Interface discovery varies between ASA and Firepower software versions, so the tool requests the interface explicitly instead of guessing it.

## Interpreting results

- `TRAFFIC ALLOWED`: packet-tracer reported `Action: allow`
- `TRAFFIC DROPPED`: packet-tracer reported `Action: drop`
- An undetermined result requires reviewing the complete output

A dropped result does not always mean that a new ACL rule is required. NAT, routing, inspection, VPN and other processing phases may cause the drop.

## Security

Use this tool only on devices where you have explicit authorization.

Credentials are requested interactively and are not stored. Avoid publishing packet-tracer output because it may contain interface names, addresses, ACLs and other infrastructure details.

## Disclaimer

Validate results using firewall logs and the device configuration before making production changes.
