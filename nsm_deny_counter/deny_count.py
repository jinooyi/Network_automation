from collections import Counter

deny_alerts_by_src = Counter()

with open("nsm.log", "r") as f:
    for line in f:
        parts = line.strip().split()

        record = {}
        for p in parts[1:]:          
            key, value = p.split("=")
            record[key] = value

        if record.get("ACTION") == "DENY":
            deny_alerts_by_src[record["SRC"]] += 1

for src, count in deny_alerts_by_src.items():
    print(f"{src}: {count} DENY alerts")
