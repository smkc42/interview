from collections import deque

from dsa.datastructures import ListNode, TreeNode


# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    def util(node: TreeNode | None) -> tuple[TreeNode | None, bool, bool]:
        if node is None:
            return (None, False, False)
        left, leftp, leftq = util(node.left)
        if leftp and leftq:
            return (left, True, True)
        right, rightp, rightq = util(node.right)
        if rightp and rightq:
            return (right, True, True)
        has_p = node == p or leftp or rightp
        has_q = node == q or leftq or rightq
        return (node if has_p and has_q else None, has_p, has_q)

    node, has_p, has_q = util(root)
    assert has_p and has_q and node is not None
    return node


# https://leetcode.com/problems/merge-intervals/
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    >>> merge([[1, 3], [2, 6], [8, 10], [15, 18]])
    [[1, 6], [8, 10], [15, 18]]
    >>> merge([[1, 4], [4, 5]])
    [[1, 5]]
    >>> merge([[4, 7], [1, 4]])
    [[1, 7]]
    """
    intervals.sort()
    merged: list[list[int]] = []
    cur_start, cur_end = intervals[0]
    for start, end in intervals[1:]:
        if start > cur_end:
            merged.append([cur_start, cur_end])
            cur_start, cur_end = start, end
        else:
            cur_end = max(cur_end, end)
    merged.append([cur_start, cur_end])
    return merged


# https://leetcode.com/problems/permutations/
def permute(nums: list[int]) -> list[list[int]]:
    """
    >>> permute([1, 2, 3])
    [[1, 2, 3], [2, 1, 3], [2, 3, 1], [1, 3, 2], [3, 1, 2], [3, 2, 1]]
    >>> permute([0, 1])
    [[0, 1], [1, 0]]
    >>> permute([1])
    [[1]]
    """
    if len(nums) <= 1:
        return [nums]
    rest = permute(nums[1:])
    res: list[list[int]] = []
    for perm in rest:
        for pos in range(len(perm) + 1):
            res.append(perm[:pos] + [nums[0]] + perm[pos:])
    return res


# https://leetcode.com/problems/combination-sum/
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    >>> combination_sum([2, 3, 6, 7], 7)
    [[7], [2, 2, 3]]
    >>> combination_sum([2, 3, 5], 8)
    [[3, 5], [2, 3, 3], [2, 2, 2, 2]]
    """
    if len(candidates) == 0:
        return [[]] if target == 0 else []
    cur: list[int] = []
    res: list[list[int]] = []
    while (cursum := sum(cur)) <= target:
        rest = combination_sum(candidates[1:], target - cursum)
        if len(rest) > 0:
            for r in rest:
                res.append(cur + r)
        cur.append(candidates[0])
    return res


# https://leetcode.com/problems/search-in-rotated-sorted-array/
def search(nums: list[int], target: int) -> int:
    """
    >>> search([4, 5, 6, 7, 0, 1, 2], 0)
    4
    >>> search([4, 5, 6, 7, 0, 1, 2], 3)
    -1
    >>> search([1], 0)
    -1
    """
    left, right, boundary = 0, len(nums) - 1, -1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] <= nums[-1]:
            boundary = mid
            right = mid - 1
        else:
            left = mid + 1
    assert boundary != -1
    left, right = (boundary, len(nums) - 1) if target <= nums[-1] else (0, boundary - 1)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


# https://leetcode.com/problems/rotting-oranges/
def oranges_rotting(grid: list[list[int]]) -> int:
    """
    >>> oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]])
    4
    >>> oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]])
    -1
    >>> oranges_rotting([[0, 2]])
    0
    """
    rows, cols = len(grid), len(grid[0])
    q: deque[tuple[int, int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c, 0))
    mins = 0
    while len(q) > 0:
        r, c, m = q.popleft()
        mins = max(mins, m)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                q.append((nr, nc, m + 1))
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                return -1
    return mins


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
