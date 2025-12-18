import json

INPUT_FILE = "router_info.json"
OS_VERSION_THRESHOLD = 12
BGP_NEIGHBOR_THRESHOLD = 50


def load_routers(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data["routers"]


def find_risky_routers(routers):
    risky = []

    for router in routers:
        if (
            router["os_version"] < OS_VERSION_THRESHOLD
            and router["bgp_neighbors"] > BGP_NEIGHBOR_THRESHOLD
        ):
            risky.append(router)

    return risky


def main():
    routers = load_routers(INPUT_FILE)
    risky_routers = find_risky_routers(routers)

    print("=== Routers requiring attention ===")
    for r in risky_routers:
        print(
            f"{r['hostname']} | "
            f"OS {r['os_version']} | "
            f"BGP neighbors {r['bgp_neighbors']}"
        )

    print(f"\nTotal affected routers: {len(risky_routers)}")


if __name__ == "__main__":
    main()
