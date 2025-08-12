import json
from pathlib import Path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generate summary for nyu logs")
    parser.add_argument("--log-dir", required=True)
    args = parser.parse_args()

    trajs = Path(args.log_dir).glob("20*.json")
    summaryf = Path(args.log_dir) / "summary.json"
    if summaryf.exists():
        summary = json.loads(summaryf.open().read())
        if "results" not in summary:
            summary["results"] = {}
    else:
        summary = {"results": {}} # Fill in info later

    for trajfn in trajs:
        traj = json.loads(trajfn.open().read())
        name = trajfn.stem
        summary["results"][name] = traj["success"]

    summaryf.open("w").write(json.dumps(summary))
