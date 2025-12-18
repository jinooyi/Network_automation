
## Purpose
Analyze NSM logs to count DENY events per source IP, enabling quick
identification of devices generating excessive blocked traffic.

#### deny_count.py
    from collections import Counter
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE_DIR, "nsm.log")


    def count_deny_events(logfile):
        deny_by_src = Counter()

        with open(logfile, "r") as f:
            for line in f:
                parts = line.strip().split()

                record = {}
                for p in parts[1:]:
                    if "=" in p:
                        key, value = p.split("=", 1)
                        record[key] = value

                if record.get("ACTION") == "DENY":
                    src_ip = record.get("SRC")
                    if src_ip:
                        deny_by_src[src_ip] += 1

        return deny_by_src


    def main():
        deny_counts = count_deny_events(LOG_FILE)

        print("=== DENY events by source IP ===")
        for src, count in deny_counts.most_common():
            print(f"{src} : {count}")

        print(f"\nTotal unique sources: {len(deny_counts)}")


    if __name__ == "__main__":
        main()


## Result

    === DENY events by source IP ===
    10.0.1.5 : 2

    Total unique sources: 1
    PS C:\Users\yijinr\Desktop\NDE_Automation> 