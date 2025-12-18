🔹 Purpose

This project demonstrates a simple network automation workflow:
Generate a fleet of router devices in a JSON inventory
Simulate BGP attributes such as OS version, ASN, and session state
Identify devices affected by a known software bug
Apply targeted BGP remediation logic
Export updated device state and a remediation report

🔹 Part 1: Generate Router Inventory (JSON)
Description:  This script generates 100 router devices and stores them in a JSON file.
Each router includes:

    1. OS version
    2. Hostname, IP, MAC address
    3. BGP neighbor information (type, ASN, session state)
    This simulates a realistic router inventory used for automation.

### Script: generate_devices.py

'''python

import json
import random

devices = []

for i in range(1, 101):
    version = random.choice([1232, 1233, 1234, 1235])
    bgp_type = random.choice(["iBGP", "eBGP"])
    asn = random.randint(64512, 70000)
    state = random.choice(["Idle", "Active", "Established"])

    devices.append({
        "name": f"R{i}",
        "hostname": f"router-{i:03}",
        "ip": f"10.0.0.{i}",
        "mac": f"AA:BB:CC:DD:EE:{i:02X}",
        "version": version,
        "bgp_neighbors": [
            {
                "neighbor_ip": f"192.0.2.{i}",
                "type": bgp_type,
                "asn": asn,
                "state": state
            }
        ]
    })

with open("devices.json", "w") as f:
    json.dump({"devices": devices}, f, indent=2)

print("devices.json generated")

'''

## Part 2: BGP Remediation Automation
Description: 
This script simulates remediation of a known software bug:

Devices running OS versions older than 1234
with eBGP neighbors using 32-bit ASNs
require a BGP soft clear when the session comes up.

The script:

Reads the generated device inventory
Identifies affected BGP sessions
Simulates a soft clear action



'''python

import json
from copy import deepcopy

INPUT_FILE = "devices.json"
OUTPUT_UPDATED_FILE = "devices_updated.json"
OUTPUT_REPORT_FILE = "remediation_report.json"
BUG_VERSION = 1234


def is_32bit_asn(asn: int) -> bool:
    return asn > 65535


def session_came_up(old_state: str, new_state: str) -> bool:
    return old_state != "Established" and new_state == "Established"


def soft_clear(device_name: str, neighbor_ip: str):
    print(f"[ACTION] clear bgp {neighbor_ip} soft in  # on {device_name}")


def load_devices(filename: str):
    with open(filename, "r") as f:
        return json.load(f)["devices"]


def save_json(filename: str, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def remediate(devices):
    remediation_report = []

    for device in devices:
        if device["version"] >= BUG_VERSION:
            continue

        for neighbor in device.get("bgp_neighbors", []):
            if neighbor["type"] != "eBGP":
                continue

            if not is_32bit_asn(neighbor["asn"]):
                continue

            old_state = neighbor["state"]
            neighbor["state"] = "Established"

            if session_came_up(old_state, neighbor["state"]):
                soft_clear(device["name"], neighbor["neighbor_ip"])

                remediation_report.append({
                    "device": device["name"],
                    "hostname": device["hostname"],
                    "neighbor_ip": neighbor["neighbor_ip"],
                    "asn": neighbor["asn"],
                    "old_state": old_state,
                    "new_state": neighbor["state"],
                    "reason": "version<1234 + eBGP + 32bit ASN + session up"
                })

    return remediation_report


if __name__ == "__main__":
    original_devices = load_devices(INPUT_FILE)
    devices = deepcopy(original_devices)

    report = remediate(devices)

    print("\n=== REMEDIATION SUMMARY ===")
    print(f"Total sessions remediated: {len(report)}")
    for r in report:
        print(f"- {r['device']} | {r['neighbor_ip']} | {r['old_state']} -> {r['new_state']}")

    save_json(OUTPUT_UPDATED_FILE, {"devices": devices})
    save_json(OUTPUT_REPORT_FILE, {"remediations": report})

    print("\n[FILES GENERATED]")
    print(f"- {OUTPUT_UPDATED_FILE}")
    print(f"- {OUTPUT_REPORT_FILE}")

'''

## Output Files

devices.json – original generated inventory
devices_updated.json – inventory after remediation
remediation_report.json – summary of remediated BGP sessions

