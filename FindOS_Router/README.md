## Purpose

This project identifies routers running specific OS versions and simulates
automation workflows based on BGP attributes, such as session type, ASN,
and state.

#### find_os_router.py

    import json
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_FILE = os.path.join(BASE_DIR, "router_info.json")


    OS_VERSION_THRESHOLD = 12
    BGP_NEIGHBOR_THRESHOLD = 50


    def load_routers(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data["routers"]

    def find_matching_routers(routers):
        matched = []

        for router in routers:
            if (
                router["os_version"] < OS_VERSION_THRESHOLD
                and router["bgp_neighbors"] > BGP_NEIGHBOR_THRESHOLD
            ):
                matched.append(router)

        return matched


    def main():
        routers = load_routers(INPUT_FILE)
        matched_routers = find_matching_routers(routers)

        print("=== Routers matching criteria ===")
        for r in matched_routers:
            print(
                f"{r['hostname']} | "
                f"OS {r['os_version']} | "
                f"BGP neighbors {r['bgp_neighbors']}"
            )

        print(f"\nTotal matched routers: {len(matched_routers)}")


    if __name__ == "__main__":
        main()



## Result
    === Routers matching criteria ===
    rtr-001 | OS 11.5 | BGP neighbors 72
    rtr-003 | OS 11.9 | BGP neighbors 55

    Total matched routers: 2
    PS C:\Users\yijinr\Desktop\NDE_Automation> 

