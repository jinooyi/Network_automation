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
        print(
            f"- {r['device']} | {r['neighbor_ip']} | "
            f"{r['old_state']} -> {r['new_state']}"
        )


    save_json(OUTPUT_UPDATED_FILE, {"devices": devices})

    save_json(OUTPUT_REPORT_FILE, {"remediations": report})

    print("\n[FILES GENERATED]")
    print(f"- {OUTPUT_UPDATED_FILE}")
    print(f"- {OUTPUT_REPORT_FILE}")
