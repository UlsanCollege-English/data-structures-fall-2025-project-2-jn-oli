"""
Utility functions for reading and writing simple (word, score) CSV data.

Each line in the CSV contains:
    word,score
No header is used.
"""

import csv


def load_csv(file_path):
    """
    Read a UTF-8 CSV file of word–score pairs and return a list of tuples.

    Invalid or missing scores default to 0.0.
    Blank lines are skipped.
    """
    pairs = []
    try:
        with open(file_path, mode="r", encoding="utf-8", newline="") as f:
            for row in csv.reader(f):
                if not row:
                    continue

                # normalize word text
                word = row[0].strip().lower()

                # parse score safely
                try:
                    score = float(row[1]) if len(row) > 1 else 0.0
                except ValueError:
                    score = 0.0

                pairs.append((word, score))

    except FileNotFoundError:
        print(f"ERROR: could not find file '{file_path}'")
        return []
    except OSError as e:
        print(f"ERROR: failed to open '{file_path}': {e}")
        return []

    return pairs


def save_csv(file_path, data):
    """
    Write (word, score) pairs to a CSV file in UTF-8 encoding.
    Overwrites the file if it already exists.
    """
    try:
        with open(file_path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for w, s in data:
                writer.writerow([w, s])
    except OSError as e:
        print(f"ERROR: failed to write '{file_path}': {e}")
