"""
Trie data structure for autocomplete and prefix lookups.

Expected public interface:
  class Trie
    - insert(word: str, freq: float)
    - remove(word: str) -> bool
    - contains(word: str) -> bool
    - complete(prefix: str, k: int) -> list[str]
    - stats() -> tuple[int, int, int]  # (word_count, height, node_count)
    - items() -> list[tuple[str, float]]
"""

import heapq


class _Node:
    """A lightweight Trie node storing children, word flag, and frequency."""
    __slots__ = ("next", "end", "score")

    def __init__(self):
        self.next = {}     # char → _Node
        self.end = False   # does this node mark a word ending?
        self.score = 0.0   # only valid if end=True


class Trie:
    """Trie (prefix tree) supporting fast autocomplete operations."""

    def __init__(self):
        self.root = _Node()
        self._count_words = 0
        self._count_nodes = 1  # root itself

    # ---------- internal helpers ----------

    def _trace(self, text: str):
        """Follow a path down the trie for a given text. Return (node, path)."""
        node = self.root
        path = [(node, '')]
        for ch in text:
            nxt = node.next.get(ch)
            if nxt is None:
                return None, []
            node = nxt
            path.append((node, ch))
        return node, path

    # ---------- core API ----------

    def insert(self, word: str, freq: float):
        """
        Insert a word with its frequency (updating if it already exists).

        Complexity: O(L) where L = len(word)
        """
        node = self.root
        for ch in word:
            if ch not in node.next:
                node.next[ch] = _Node()
                self._count_nodes += 1
            node = node.next[ch]

        if not node.end:
            self._count_words += 1
        node.end = True
        node.score = freq

    def remove(self, word: str) -> bool:
        """
        Remove a word from the trie if present. Returns True if removed.

        Complexity: O(L)
        """
        node, path = self._trace(word)
        if not node or not node.end:
            return False

        node.end = False
        node.score = 0.0
        self._count_words -= 1

        # prune unused nodes
        # Note: path[i] is (current_node, incoming_char_for_current)
        #       path[i-1] is (parent_node, incoming_char_for_parent)
        for i in range(len(path) - 1, 0, -1):
            parent_node, _ = path[i - 1]
            current_node, current_char = path[i]
            # If current node still used (has children or marks another word), stop.
            if current_node.next or current_node.end:
                break
            # delete the key in parent that points to current
            if current_char in parent_node.next:
                del parent_node.next[current_char]
                self._count_nodes -= 1
            else:
                # Defensive: if the mapping is absent, stop pruning
                break

        return True

    def contains(self, word: str) -> bool:
        """Check whether an exact word exists."""
        node, _ = self._trace(word)
        return bool(node and node.end)

    def complete(self, prefix: str, k: int):
        """
        Return up to k best word completions for a given prefix.

        Sorting priority:
          - Highest frequency first
          - Alphabetical order for ties

        Complexity: O(M + N log K)
        """
        node, _ = self._trace(prefix)
        if not node:
            return []

        heap = []  # (freq, word)

        def dfs(n: _Node, word: str):
            if n.end:
                pair = (n.score, word)
                if len(heap) < k:
                    heapq.heappush(heap, pair)
                else:
                    heapq.heappushpop(heap, pair)

            for c in sorted(n.next.keys()):
                dfs(n.next[c], word + c)

        dfs(node, prefix)

        # sort by freq desc, word asc
        results = sorted(heap, key=lambda x: (-x[0], x[1]))
        return [w for _, w in results]

    def stats(self):
        """
        Return (word_count, height, node_count).

        Height = length of the longest path from root to leaf.
        Complexity: O(T)
        """

        def depth(n: _Node):
            if not n.next:
                return 0
            return 1 + max(depth(child) for child in n.next.values())

        return self._count_words, depth(self.root), self._count_nodes

    def items(self):
        """
        Return all (word, freq) pairs currently stored.

        Complexity: O(T)
        """
        output = []

        def gather(n: _Node, text: str):
            if n.end:
                output.append((text, n.score))
            for c, nxt in n.next.items():
                gather(nxt, text + c)

        gather(self.root, "")
        return output
