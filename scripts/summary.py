import json
from pathlib import Path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Log summary")
    parser.add_argument("-l", "--log-dir", required=True, help="Logs directory")
    parser.add_argument("-m", "--model", required=True, help="Exact model string")
    parser.add_argument("-d", "--dataset", required=True, help="Dataset JSON")
    args = parser.parse_args()

    logdir = Path(args.log_dir)
    dataset = json.loads(Path(args.dataset).open().read())
    model = args.model

    results = {}

    for chal, info in dataset.items():
        path = logdir / info["path"][5:]
        results[chal] = False
        if not path.is_dir():
            continue

        found = 0
        for i in range(1, 6):
            convo = path / f"conversation.{model}.{i}.json"
            if not convo.is_file():
                continue
            try:
                convo = json.loads(convo.open().read())
            except json.JSONDecodeError:
                continue
            found += 1
            if convo["solved"]:
                results[chal] = True
        if found == 0:
            print("[WARN] Logs not found for", chal, model)
    (logdir / "summary.json").open("w").write(json.dumps({"results": results}))
