import json
import random

devices = []

for i in range(1, 101):
    version = random.choice([1232, 1233, 1234, 1235])
    bgp_type = random.choice(["iBGP", "eBGP"])
    asn = random.randint(64512, 70000)   # 일부는 32-bit
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

print("devices.json 생성 완료")
