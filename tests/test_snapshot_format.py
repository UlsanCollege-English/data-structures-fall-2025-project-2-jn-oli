# tests/test_snapshot_format.py
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'words.csv'


def test_snapshot_exists_and_has_50000_lines():
    assert DATA.exists(), "data/words.csv is missing — generate it with scripts/make_wordlist.py and commit it."
    # Count non-empty lines
    n = 0
    with DATA.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                n += 1
    assert n == 50_000, f"Expected exactly 50,000 lines in data/words.csv, found {n}."