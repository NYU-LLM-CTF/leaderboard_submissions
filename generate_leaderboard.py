import json
from pathlib import Path

from nyuctf.dataset import CTFDataset
from nyuctf.utils import CATEGORY_SHORT

REPOSITORY = "https://github.com/NYU-LLM-CTF/leaderboard_submissions/tree/main/"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Generate leaderboard.json")
    parser.add_argument("--dataset", required=True, help="Dataset JSON")
    
    args = parser.parse_args()

    basedir = Path(__file__).parent
    transcripts = basedir / "transcripts"
    submissions = transcripts.glob("*/summary.json")

    dataset = CTFDataset(args.dataset)

    leaderboard = {
        "dataset": {cat: len(list(dataset.filter(category=cat))) for cat in CATEGORY_SHORT},
        "submissions":[]
    }
    leaderboard["dataset"]["total"] = len(dataset)

    for submission in submissions:
        folder = submission.parent.name
        print("Processing", folder)
        try:
            summary = json.loads(submission.open().read())
        except JSONDecodeError:
            print("... Error parsing JSON! skipping")
            continue
        if "metadata" not in summary:
            print("... Metadata not found! skipping")
            continue
        if "results" not in summary:
            print("... Results not found! skipping")
            continue
        metadata = summary["metadata"]
        results = summary["results"]

        total = 0
        per_category = {c:0 for c in CATEGORY_SHORT}

        for chal in map(lambda n: dataset.get(n[0]), filter(lambda n: n[1], results.items())):
            total += 1
            per_category[chal["category"]] += 1

        leaderboard["submissions"].append({
            "name": metadata["agent"],
            "comment": metadata["comment"],
            "logs": REPOSITORY + str(submission.relative_to(basedir)),
            "link": metadata["link"],
            "model": metadata["model"],
            "solved": total,
            "per_category": per_category,
        })

    (basedir / "leaderboard.json").open("w").write(json.dumps(leaderboard))
