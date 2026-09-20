from __future__ import annotations

from collections.abc import Callable

from dsa.datastructures import GraphNode


# https://leetcode.com/problems/coin-change/
def coin_change(coins: list[int], amt: int) -> int:
    """
    >>> coin_change([1, 2, 5], 11)
    3
    >>> coin_change([2], 3)
    -1
    >>> coin_change([1], 0)
    0
    """
    memo: list[int] = [-1] * (amt + 1)
    memo[0] = 0
    for a in range(1, amt + 1):
        for c in coins:
            if a - c >= 0 and memo[a - c] != -1:
                cur = memo[a - c] + 1
                memo[a] = cur if memo[a] == -1 else min(memo[a], cur)
    return memo[amt]


# https://leetcode.com/problems/implement-trie-prefix-tree/
class Trie:
    """
    >>> t = Trie()
    >>> t.insert("apple")
    >>> t.search("apple")
    True
    >>> t.search("app")
    False
    >>> t.starts_with("app")
    True
    >>> t.insert("app")
    >>> t.search("app")
    True
    """

    class Node:
        def __init__(
            self,
            chr: str,
            end: bool = False,
            children: dict[str, Trie.Node] | None = None,
        ):
            self.chr = chr
            self.end = end
            self.children = children if children is not None else {}

    def __init__(self):
        self.root = Trie.Node("")

    def insert(self, word: str) -> None:
        ptr = self.root
        for chr in word:
            if chr not in ptr.children:
                ptr.children[chr] = Trie.Node(chr)
            ptr = ptr.children[chr]
        ptr.end = True

    def search(self, word: str) -> bool:
        ptr = self.root
        for chr in word:
            if chr not in ptr.children:
                return False
            ptr = ptr.children[chr]
        return ptr.end

    def starts_with(self, prefix: str) -> bool:
        ptr = self.root
        for chr in prefix:
            if chr not in ptr.children:
                return False
            ptr = ptr.children[chr]
        return True


# https://leetcode.com/problems/course-schedule/
def can_finish(n: int, prereqs: list[list[int]]) -> bool:
    """
    >>> can_finish(2, [[1, 0]])
    True
    >>> can_finish(2, [[1, 0], [0, 1]])
    False
    >>> can_finish(20, [[0, 10], [3, 18], [5, 5], [6, 11], [11, 14], [13, 1], [15, 1], [17, 4]])
    False
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in prereqs:
        adj[b].append(a)

    visited: list[bool] = [False] * n
    stack: set[int] = set()

    def has_cycle(x: int) -> bool:
        if visited[x]:
            return False
        if x in stack:
            return True
        stack.add(x)
        for nbr in adj[x]:
            if has_cycle(nbr):
                return True
        stack.remove(x)
        visited[x] = True
        return False

    for x in range(n):
        if not visited[x] and has_cycle(x):
            return False
    return True


# https://leetcode.com/problems/evaluate-reverse-polish-notation/
def eval_rpn(tokens: list[str]) -> int:
    """
    >>> eval_rpn(["2", "1", "+", "3", "*"])
    9
    >>> eval_rpn(["4", "13", "5", "/", "+"])
    6
    >>> eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"])
    22
    """
    stack: list[int] = []
    ops: dict[str, Callable[[int, int], int]] = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: int(x / y),
    }
    for tok in tokens:
        if tok in ops:
            second = stack.pop()
            first = stack.pop()
            stack.append(ops[tok](first, second))
        else:
            stack.append(int(tok))
    return stack[0]


# https://leetcode.com/problems/clone-graph/
def clone_graph(node: GraphNode | None) -> GraphNode | None:
    """
    >>> GraphNode.to_list(clone_graph(GraphNode.from_list([[2, 4], [1, 3], [2, 4], [1, 3]])))
    [[2, 4], [1, 3], [2, 4], [1, 3]]
    >>> GraphNode.to_list(clone_graph(GraphNode.from_list([[]])))
    [[]]
    >>> GraphNode.to_list(clone_graph(GraphNode.from_list([])))
    []
    """
    if node is None:
        return None

    cloned: dict[GraphNode, GraphNode] = {}

    def util(n: GraphNode):
        for nbr in n.neighbors:
            if nbr not in cloned:
                cloned[nbr] = GraphNode(nbr.val)
                util(nbr)
            cloned[n].neighbors.append(cloned[nbr])

    cloned[node] = GraphNode(node.val)
    util(node)
    return cloned[node]
