# NYU CTF Dataset Leaderboard

This repository contains the submissions for the NYU CTF Dataset [leaderboard](https://nyu-llm-ctf.github.io).

## How to submit

1. Fork this repository
2. Clone your forked repository - use `git clone --depth 1` to avoid pulling the entire history as it can be large
3. Create a folder under `transcripts/` with a unique descriptive name:
4. The folder should contain the following:
    1. A `summary.json` with the success result of each challenge and submission metadata (see structure below)
    2. The agent conversation transcripts or logs (see details below)
    3. A README that describes your submission, the format of your log files, and provides a point of contact
5. Each folder under `transcripts/` containing a valid `summary.json` is considered a submission
6. After creating your folder, generate the `leaderboard.json` (described below) to verify if your submission is processed correctly
7. Finally, create a PR to the main repository with your submission

*Note: DO NOT add the generated `leaderboard.json` to your PR.*

### `summary.json` structure

```
{
  "metadata": {
    "agent": ...,
    "comment": ...,
    "model": ...,
    "link": ...,
    "date": ...
  },
  "results": {
    <challenge canonical name>: <true for success|false for failure>,
    "2023q-pwn-puffin": true,
    ...
  }
}
```

The metadata should contain the following fields:

- `agent`: The agent name
- `comment`: A short comment to describe the results, e.g. "pass@5" (leave empty if not needed)
- `model`: Exact model string with date stamp, e.g. gpt-4-0125-preview
- `link`: Link to agent repository or documentation
- `date`: Date of submission in "YYYY/MM/DD" format

The results should contain success or failure for each challenge of the dataset.
The challenge canonical name can be generated with the `nyuctf` package using `CTFChallenge.canonical_name`.
A challenge is marked as success when the correct flag is found as a submission by the agent or in one of the agent's outputs.
Otherwise, it is marked as failure. Missing or errored runs are marked as failure.
There should be an entry for all 200 challenges of the dataset.

### Transcript or log structure

You have freedom to decide the file format and structure of the logs, but it must contain the following minimal information:
- Conversational history containing the initial prompt, outputs by the LLM, commands executed and their output
- Timestamp of when the transcript was generated
- Indicator of whether the correct flag was found or not

Please describe the transcript format in the README of your submission.
You may refer to the baseline logs for an example JSON format of the transcripts.

## Generating `leaderboard.json`

`leaderboard.json` is the file that accumulates all leaderboard submissions, and is loaded by the leaderboard webpage.

Run the `generate_leaderboard.py` script to generate it.

```
python3 generate_leaderboard.py --dataset ~/NYU_CTF_Bench/test_dataset.json
```
