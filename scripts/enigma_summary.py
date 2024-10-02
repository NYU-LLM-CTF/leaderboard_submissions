import json
from pathlib import Path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generate summary for enigma logs")
    parser.add_argument("--dataset", required=True)
    args = parser.parse_args()

    nicename = lambda s: s['category'] + "_" + s['challenge'].replace(" ", "").replace("?", "").replace("'", "").replace("-", "").replace("_", "").lower()
    dataset = json.loads(Path(args.dataset).open().read())
    results = {chal: False for chal in dataset}
    dataset = {nicename(data): chal for chal, data in dataset.items()}

    trajs = Path(".").glob("*.traj")
    for trajfn in trajs:
        traj = json.loads(trajfn.open().read())
        if traj["info"]["exit_status"] != "submitted":
            continue

        name = trajfn.stem.lower()
        if name not in dataset:
            print("Trajectory not in dataset!", trajfn.stem)
            continue
        results[dataset[name]] = True

    Path("summary.json").open("w").write(json.dumps({"results": results}))
