from collections.abc import Callable

from dsa.datastructures import GraphNode


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
