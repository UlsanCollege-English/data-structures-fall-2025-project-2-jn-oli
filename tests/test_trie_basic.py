# tests/test_trie_basic.py
from src.trie import Trie
from pathlib import Path
from src.io_utils import load_csv

RES = Path(__file__).parent / 'resources' / 'small_words.csv'

# 4 normal tests

def test_insert_and_contains_basic():
    t = Trie()
    t.insert('hello', 5)
    assert t.contains('hello')


def test_complete_prefix_basic():
    t = Trie()
    for w, s in load_csv(RES):
        t.insert(w, s)
    assert t.complete('he', 3) == ['hello', 'help', 'hell']


def test_tie_break_lexicographic():
    t = Trie()
    t.insert('aa', 1.0)
    t.insert('ab', 1.0)
    t.insert('ac', 1.0)
    assert t.complete('a', 3) == ['aa', 'ab', 'ac']


def test_remove_then_missing():
    t = Trie()
    t.insert('toast', 1)
    assert t.remove('toast') is True
    assert t.contains('toast') is False

# 3 edge-case tests

def test_complete_empty_prefix_returns_top_k_or_define_behavior():
    t = Trie()
    for w, s in load_csv(RES):
        t.insert(w, s)
    out = t.complete('', 2)
    # You may choose behavior; test assumes top-k overall
    assert out == ['hello', 'help']


def test_nonexistent_prefix():
    t = Trie()
    for w, s in load_csv(RES):
        t.insert(w, s)
    assert t.complete('xyz', 5) == []


def test_remove_nonexistent():
    t = Trie()
    assert t.remove('missing') is False

# 3 more complicated tests

def test_large_k_truncates():
    t = Trie()
    for w, s in load_csv(RES):
        t.insert(w, s)
    out = t.complete('he', 100)
    assert out[:5] == ['hello', 'help', 'hell', 'helmet', 'heap']


def test_stats_shape_changes():
    t = Trie()
    for w, s in load_csv(RES):
        t.insert(w, s)
    words, height, nodes = t.stats()
    assert words >= 10
    assert nodes >= words  # nodes count includes internal nodes
    assert height >= 1


def test_update_frequency_affects_ranking():
    t = Trie()
    t.insert('hello', 1)
    t.insert('helium', 10)
    out = t.complete('he', 2)
    assert out == ['helium', 'hello']