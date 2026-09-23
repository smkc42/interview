from collections import deque

from dsa.datastructures import ListNode, TreeNode


# https://leetcode.com/problems/number-of-islands/
def num_islands(grid: list[list[str]]) -> int:
    """
    >>> num_islands([
    ...   ["1","1","1","1","0"],
    ...   ["1","1","0","1","0"],
    ...   ["1","1","0","0","0"],
    ...   ["0","0","0","0","0"]
    ... ])
    1
    >>> num_islands([
    ...   ["1","1","0","0","0"],
    ...   ["1","1","0","0","0"],
    ...   ["0","0","1","0","0"],
    ...   ["0","0","0","1","1"]
    ... ])
    3
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    islands = 0
    for sr in range(rows):
        for sc in range(cols):
            if visited[sr][sc] or grid[sr][sc] == "0":
                continue
            islands += 1
            visited[sr][sc] = True
            q = deque([(sr, sc)])
            while len(q) > 0:
                r, c = q.popleft()
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if visited[nr][nc] or grid[nr][nc] == "0":
                            continue
                        visited[nr][nc] = True
                        q.append((nr, nc))
    return islands


# https://leetcode.com/problems/validate-binary-search-tree/
def is_valid_bst(root: TreeNode | None) -> bool:
    """
    >>> is_valid_bst(TreeNode.from_list([2, 1, 3]))
    True
    >>> is_valid_bst(TreeNode.from_list([5, 1, 4, None, None, 3, 6]))
    False
    """

    def util(node: TreeNode) -> tuple[bool, int, int]:
        min = max = node.val
        if node.left is not None:
            left_valid, min, left_max = util(node.left)
            if not left_valid or left_max >= node.val:
                return (False, -1, -1)
        if node.right is not None:
            right_valid, right_min, max = util(node.right)
            if not right_valid or right_min <= node.val:
                return (False, -1, -1)
        return (True, min, max)

    if root is None:
        raise RuntimeError("invalid input")
    valid, _, _ = util(root)
    return valid


# https://leetcode.com/problems/reverse-linked-list/
def reverse_list(head: ListNode | None) -> ListNode | None:
    """
    >>> ListNode.to_list(reverse_list(ListNode.from_list([1, 2, 3, 4, 5])))
    [5, 4, 3, 2, 1]
    >>> ListNode.to_list(reverse_list(ListNode.from_list([1, 2])))
    [2, 1]
    >>> ListNode.to_list(reverse_list(ListNode.from_list([])))
    []
    """
    if head is None:
        return None
    prev: ListNode | None = None
    ptr = head
    while ptr is not None:
        tmp = ptr.next
        ptr.next = prev
        prev = ptr
        ptr = tmp
    return prev
