# Firewall Toolkit

Python tools for firewall validation, connectivity testing and network troubleshooting.

## Tools

### Connectivity Checker

Tests network connections and identifies successful, refused and timed-out connection attempts.

- [Documentation](./connectivity-checker/)
- Language: Python
- Purpose: Assist with firewall rule validation and connectivity troubleshooting

### Cisco ASA Rule Checker

Validates firewall rules and connectivity behavior in Cisco ASA environments.

- [Documentation](./cisco-asa/)
- Language: Python
- Purpose: Support Cisco ASA firewall rule verification and troubleshooting

### Check Point Rule Checker

Utilities for checking firewall rules in Check Point environments.

- [Documentation](./checkpoint/)
- Language: Python
- Purpose: Support Check Point firewall rule verification and troubleshooting

## Requirements

Requirements vary by tool. See the documentation inside each directory.

General requirements may include:

- Python 3.10+
- Access to an authorized network environment
- Network connectivity to the tested destination
- Valid firewall management credentials, when required

## Installation

```bash
git clone https://github.com/pauloink/firewall-toolkit.git
cd firewall-toolkit
