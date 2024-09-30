import json
from pathlib import Path

MAX_LEN = 100000 # 100K

def truncate(log):
    print("Truncating", log)
    data = json.loads(log.open("r").read())
    if "debug_log" in data:
        del data["debug_log"]
    for msg in data["messages"]:
        if "content" in msg[1] and msg[1]["content"] and len(msg[1]["content"]) > MAX_LEN:
            msg[1]["content"] = msg[1]["content"][:MAX_LEN] + "...<truncated>"
    log.open("w").write(json.dumps(data))

alllogs = Path(".").glob("**/conversation.*.json")
for log in alllogs:
    truncate(log)
