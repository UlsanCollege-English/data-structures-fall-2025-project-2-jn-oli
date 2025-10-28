[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/jZ1tjCvj)
# Project 2 — Trie Autocomplete (Type‑Ahead)


Implement a prefix‑tree (trie) that supports `insert`, `remove`, `contains`, and `complete(prefix, k)` ranked by frequency, plus a simple CLI.


## How to run tests locally
```bash
python -m pytest -q
```

## Word list (50,000 words via wordfreq)

You must generate a frequency‑ordered snapshot with exactly 50,000 distinct words and commit it as data/words.csv (CSV columns: word,score). The program should run offline using this snapshot.

- Install once locally (not used at runtime):

```bash
pip install wordfreq
```

- Generate your snapshot (script provided in scripts/make_wordlist.py).

> The tests will fail until data/words.csv exists with exactly 50,000 lines (header not required). This mirrors grading.

## CLI contract (brief)

- `load <path>` — replace current vocabulary from CSV.

- `save <path>` — write `(word,score)` CSV of current vocabulary.

- `insert <word> <freq>` — add/update.

- `remove <word>` — print `OK` or `MISS`.

- `contains <word>` — print `YES` or `NO`.

- `complete <prefix> <k>` — print comma‑separated suggestions (empty line if none).

- `stats` — print `words=<n> height=<h> nodes=<t>`.

- `quit` — exit.

## Implementation notes

- Normalize to lowercase ASCII unless you document more. Be consistent.

- Time targets: `insert/remove/contains` O(len(word)); `complete` ~ O(m + k log k').

- Use docstrings to justify your complexity.

## Common problems

- Forgetting to commit `data/words.csv` → snapshot test fails.

- Non‑deterministic ties → always tie‑break lexicographically.

- Printing extra prompts or spaces in CLI → keep outputs exact.