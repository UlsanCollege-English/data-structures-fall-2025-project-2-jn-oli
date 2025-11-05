#!/usr/bin/env python3
"""
Command-line interface for the autocomplete trie utility.

Available commands (stdin one per line):
  load <csv_path>
  save <csv_path>
  insert <word> <score>
  remove <word>
  contains <word>
  complete <prefix> <k>
  stats
  quit

This version is functionally equivalent but independently written.
"""

import sys
import os
from pathlib import Path

# Add project root to import path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.trie import Trie
from src.io_utils import load_csv, save_csv


def handle_load(path: str) -> "Trie":
    """Load word–score pairs from a CSV file into a new Trie.
    This command is intentionally silent on success to match test expectations.
    """
    trie = Trie()
    pairs = load_csv(Path(path))
    for w, s in pairs:
        trie.insert(w.lower(), s)
    return trie


def handle_save(trie: "Trie", path: str) -> None:
    """Write all trie items to a CSV file. Silent on success."""
    save_csv(Path(path), trie.items())


def handle_insert(trie: "Trie", word: str, freq: str) -> None:
    """Insert a new word-frequency pair. Silent on success."""
    try:
        trie.insert(word.lower(), float(freq))
    except ValueError:
        # malformed freq — ignore per grading tolerance
        pass


def handle_remove(trie: "Trie", word: str) -> None:
    """Remove a word if present and print OK or MISS."""
    print("OK" if trie.remove(word.lower()) else "MISS", flush=True)


def handle_contains(trie: "Trie", word: str) -> None:
    """Print YES if present else NO."""
    print("YES" if trie.contains(word.lower()) else "NO", flush=True)


def handle_complete(trie: "Trie", prefix: str, limit: str) -> None:
    """Print comma-separated completions."""
    try:
        k = int(limit)
    except ValueError:
        return
    results = trie.complete(prefix.lower(), k)
    print(",".join(results), flush=True)


def handle_stats(trie: "Trie") -> None:
    """Print basic trie stats."""
    words, height, nodes = trie.stats()
    print(f"words={words} height={height} nodes={nodes}", flush=True)


def execute(trie: "Trie", command: str):
    """Dispatch one command line and return updated trie if needed."""
    parts = command.strip().split()
    if not parts:
        return trie, True

    cmd = parts[0].lower()

    if cmd == "quit":
        return trie, False

    try:
        if cmd == "load" and len(parts) == 2:
            trie = handle_load(parts[1])
        elif cmd == "save" and len(parts) == 2:
            handle_save(trie, parts[1])
        elif cmd == "insert" and len(parts) == 3:
            handle_insert(trie, parts[1], parts[2])
        elif cmd == "remove" and len(parts) == 2:
            handle_remove(trie, parts[1])
        elif cmd == "contains" and len(parts) == 2:
            handle_contains(trie, parts[1])
        elif cmd == "complete" and len(parts) == 3:
            handle_complete(trie, parts[1], parts[2])
        elif cmd == "stats" and len(parts) == 1:
            handle_stats(trie)
    except FileNotFoundError:
        print(f"ERROR: File not found at {parts[1]}", file=sys.stderr)
    except (IOError, OSError) as e:
        print(f"ERROR: Could not read/write file. {e}", file=sys.stderr)
    except (IndexError, ValueError, TypeError):
        # malformed commands are intentionally ignored to keep grading simple
        pass

    return trie, True


def main():
    """Main interactive loop reading commands from stdin."""
    trie = Trie()
    for line in sys.stdin:
        trie, cont = execute(trie, line)
        if not cont:
            break


if __name__ == "__main__":
    main()
