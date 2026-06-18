#!/usr/bin/env python3

import getpass
import ipaddress
import re

from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)


INTERFACE_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


def read_ip(prompt):
    value = input(prompt).strip()

    try:
        return str(ipaddress.ip_address(value))
    except ValueError as error:
        raise ValueError(f"Invalid IP address: {value}") from error


def read_port(prompt):
    value = input(prompt).strip()

    try:
        port = int(value)
    except ValueError as error:
        raise ValueError("Port must be an integer") from error

    if not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535")

    return port


def read_protocol():
    protocol = input("Protocol (TCP or UDP): ").strip().lower()

    if protocol not in {"tcp", "udp"}:
        raise ValueError("Protocol must be TCP or UDP")

    return protocol


def read_interface():
    interface = input(
        "Ingress interface name (for example: inside): "
    ).strip()

    if not INTERFACE_PATTERN.fullmatch(interface):
        raise ValueError("Invalid interface name")

    return interface


def collect_connection_data():
    host = read_ip("ASA management IP: ")
    username = input("Username: ").strip()

    if not username:
        raise ValueError("Username cannot be empty")

    password = getpass.getpass("Password: ")
    enable_secret = getpass.getpass(
        "Enable secret (press Enter to reuse the password): "
    )

    if not password:
        raise ValueError("Password cannot be empty")

    return {
        "device_type": "cisco_asa",
        "host": host,
        "username": username,
        "password": password,
        "secret": enable_secret or password,
    }


def build_packet_tracer_command(
    interface,
    protocol,
    source_ip,
    source_port,
    destination_ip,
    destination_port,
):
    return (
        f"packet-tracer input {interface} {protocol} "
        f"{source_ip} {source_port} "
        f"{destination_ip} {destination_port} detailed"
    )


def run_check():
    device = collect_connection_data()

    source_ip = read_ip("Source IP: ")
    source_port = read_port("Source port: ")
    destination_ip = read_ip("Destination IP: ")
    destination_port = read_port("Destination port: ")
    protocol = read_protocol()
    ingress_interface = read_interface()

    print(f"\nConnecting to {device['host']}...")

    connection = ConnectHandler(**device)

    try:
        if device["secret"]:
            connection.enable()

        command = build_packet_tracer_command(
            ingress_interface,
            protocol,
            source_ip,
            source_port,
            destination_ip,
            destination_port,
        )

        output = connection.send_command(
            command,
            read_timeout=60,
        )

        print("\nPacket-tracer output")
        print("=" * 60)
        print(output)
        print("=" * 60)

        normalized_output = output.lower()

        if "action: allow" in normalized_output:
            print("\nResult: TRAFFIC ALLOWED")
        elif "action: drop" in normalized_output:
            print("\nResult: TRAFFIC DROPPED")

            access_groups = connection.send_command(
                "show running-config access-group"
            )

            if access_groups.strip():
                print("\nConfigured access groups:")
                print(access_groups)

            print(
                "\nReview the packet-tracer phases to identify "
                "the exact drop reason."
            )
        else:
            print(
                "\nResult: Unable to determine the final action. "
                "Review the complete output."
            )

    finally:
        connection.disconnect()


def main():
    try:
        run_check()

    except ValueError as error:
        raise SystemExit(f"Input error: {error}")

    except NetmikoAuthenticationException:
        raise SystemExit(
            "Authentication failed. Verify the username, password "
            "and enable secret."
        )

    except NetmikoTimeoutException:
        raise SystemExit(
            "Connection timed out. Verify the management address, "
            "SSH access and network connectivity."
        )

    except OSError as error:
        raise SystemExit(f"Connection error: {error}")


if __name__ == "__main__":
    main()
