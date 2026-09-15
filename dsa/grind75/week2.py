from collections import Counter, deque
from collections.abc import Callable

from dsa.datastructures import ListNode, TreeNode


# https://leetcode.com/problems/binary-tree-level-order-traversal/
def level_order(root: TreeNode | None) -> list[list[int]]:
    """
    >>> level_order([3, 9, 20, None, None, 15, 7])
    [[3], [9, 20], [15, 7]]
    >>> level_order([1])
    [[1]]
    >>> level_order([])
    []
    """
    if root is None:
        return []
    res: list[list[int]] = []
    q = deque([(root, 1)])
    while len(q) > 0:
        node, depth = q.popleft()
        if len(res) < depth:
            res.append([])
        res[-1].append(node.val)
        if node.left is not None:
            q.append((node.left, depth + 1))
        if node.right is not None:
            q.append((node.right, depth + 1))
    return res


# https://leetcode.com/problems/3sum/
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    >>> three_sum([-1, 0, 1, 2, -1, -4])
    [[-1, -1, 2], [-1, 0, 1]]
    >>> three_sum([0, 1, 1])
    []
    >>> three_sum([0, 0, 0])
    [[0, 0, 0]]
    """
    nums.sort()
    res: list[list[int]] = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i - 1] == nums[i]:
            continue
        left, right, target = i + 1, len(nums) - 1, -nums[i]
        while left < right:
            sum = nums[left] + nums[right]
            if sum < target:
                left += 1
            elif sum > target:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                right -= 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
    return res


# https://leetcode.com/problems/longest-substring-without-repeating-characters/
def length_of_longest_substring(s: str) -> int:
    """
    >>> length_of_longest_substring("abcabcbb")
    3
    >>> length_of_longest_substring("bbbbb")
    1
    >>> length_of_longest_substring("pwwkew")
    3
    """
    indices: dict[str, int] = {}
    start, end, longest = 0, 0, 0
    while end < len(s):
        if s[end] in indices and indices[s[end]] >= start:
            start = indices[s[end]] + 1
        longest = max(longest, end - start + 1)
        indices[s[end]] = end
        end += 1
    return longest


# https://leetcode.com/problems/ransom-note/
def can_construct(ransom_note: str, magazine: str) -> bool:
    """
    >>> can_construct("a", "b")
    False
    >>> can_construct("aa", "ab")
    False
    >>> can_construct("aa", "aab")
    True
    """
    mfreq = Counter(magazine)
    rfreq = Counter(ransom_note)
    for chr in rfreq:
        if chr not in mfreq or mfreq[chr] < rfreq[chr]:
            return False
    return True


# https://leetcode.com/problems/first-bad-version/
def first_bad_version(n: int, is_bad_version: Callable[[int], bool]) -> int:
    """
    >>> first_bad_version(5, lambda v: 4 <= v <= 5)
    4
    >>> first_bad_version(1, lambda v: 1 <= v <= 1)
    1
    """
    left, right, boundary = 1, n, -1
    while left <= right:
        mid = int((left + right) / 2)
        if is_bad_version(mid):
            boundary = mid
            right = mid - 1
        else:
            left = mid + 1
    return boundary


# https://leetcode.com/problems/implement-queue-using-stacks/
class MyQueue:
    """
    >>> q = MyQueue()
    >>> q.push(1)
    >>> q.push(2)
    >>> q.peek()
    1
    >>> q.pop()
    1
    >>> q.empty()
    False
    """

    def __init__(self):
        self.forward: list[int] = []
        self.reverse: list[int] = []

    def push(self, x: int) -> None:
        self.forward.append(x)

    def pop(self) -> int:
        if len(self.reverse) == 0:
            self._fill_reverse()
        return self.reverse.pop()

    def peek(self) -> int:
        if len(self.reverse) == 0:
            self._fill_reverse()
        return self.reverse[-1]

    def empty(self) -> int:
        return len(self.reverse) == 0 and len(self.forward) == 0

    def _fill_reverse(self):
        while len(self.forward) > 0:
            self.reverse.append(self.forward.pop())


# https://leetcode.com/problems/linked-list-cycle/
def has_cycle(head: ListNode | None) -> bool:
    """
    >>> tail = ListNode(-4)
    >>> cycle = ListNode(2, ListNode(0, tail))
    >>> tail.next = cycle
    >>> head = ListNode(3, cycle)
    >>> has_cycle(head)
    True
    >>> tail = ListNode(2)
    >>> cycle = ListNode(1, tail)
    >>> tail.next = cycle
    >>> head = cycle
    >>> has_cycle(head)
    True
    >>> head = ListNode(1)
    >>> has_cycle(head)
    False
    """
    slow = fast = head
    while slow is not None and fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# https://leetcode.com/problems/balanced-binary-tree/
def is_balanced(root: TreeNode | None) -> bool:
    """
    >>> is_balanced(TreeNode.from_list([3, 9, 20, None, None, 15, 7]))
    True
    >>> is_balanced(TreeNode.from_list([1, 2, 2, 3, 3, None, None, 4, 4]))
    False
    >>> is_balanced(TreeNode.from_list([]))
    True
    """

    def util(node: TreeNode | None) -> tuple[bool, int]:
        if node is None:
            return (True, 0)
        is_left_balanced, left_depth = util(node.left)
        if not is_left_balanced:
            return (False, -1)
        is_right_balanced, right_depth = util(node.right)
        if not is_right_balanced:
            return (False, -1)
        if abs(left_depth - right_depth) > 1:
            return (False, -1)
        return (True, max(left_depth, right_depth) + 1)

    is_balanced, _ = util(root)
    return is_balanced


# https://leetcode.com/problems/k-closest-points-to-origin/
def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    >>> k_closest([[1, 3], [-2, 2]], 1)
    [[-2, 2]]
    >>> k_closest([[3, 3], [5, -1], [-2, 4]], 2)
    [[3, 3], [-2, 4]]
    """
    points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
    return points[:k]


# https://leetcode.com/problems/01-matrix/
def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    """
    >>> update_matrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    >>> update_matrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]])
    [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
    """
    rows, cols = len(mat), len(mat[0])
    upd = [[-1] * cols for _ in range(rows)]
    q: deque[tuple[int, int]] = deque()
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                upd[r][c] = 0
                q.append((r, c))
    while len(q) > 0:
        r, c = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and upd[nr][nc] == -1:
                upd[nr][nc] = upd[r][c] + 1
                q.append((nr, nc))
    return upd
