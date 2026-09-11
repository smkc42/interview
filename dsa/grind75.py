from collections import Counter, deque

from datastructures import ListNode, TreeNode


# https://leetcode.com/problems/maximum-subarray/
def max_subarray(nums: list[int]) -> int:
    """
    >>> max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray([1])
    1
    >>> max_subarray([5, 4, -1, 7, 8])
    23
    """
    max_so_far = max_ending_here = nums[0]
    for n in nums[1:]:
        max_ending_here = max(max_ending_here + n, n)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far


# https://leetcode.com/problems/flood-fill/
def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    """
    >>> flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2)
    [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    >>> flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0)
    [[0, 0, 0], [0, 0, 0]]
    """
    rows, cols = len(image), len(image[0])
    orig = image[sr][sc]
    if orig == color:
        return image
    image[sr][sc] = color
    q = deque([(sr, sc)])
    while len(q) > 0:
        r, c = q.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == orig:
                image[nr][nc] = color
                q.append((nr, nc))
    return image


# https://leetcode.com/problems/binary-search/
def search(nums: list[int], target: int) -> int:
    """
    >>> search([-1, 0, 3, 5, 9, 12], 9)
    4
    >>> search([-1, 0, 3, 5, 9, 12], 2)
    -1
    >>> search([5], 5)
    0
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] > target:
            right = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            return mid
    return -1


# https://leetcode.com/problems/invert-binary-tree/
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    """
    >>> TreeNode.to_list(invert_tree(TreeNode.from_list([4, 2, 7, 1, 3, 6, 9])))
    [4, 7, 2, 9, 6, 3, 1]
    >>> TreeNode.to_list(invert_tree(TreeNode.from_list([2, 1, 3])))
    [2, 3, 1]
    >>> TreeNode.to_list(invert_tree(TreeNode.from_list([])))
    []
    """
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


# https://leetcode.com/problems/valid-anagram/
def is_anagram(s: str, t: str) -> bool:
    """
    >>> is_anagram("anagram", "nagaram")
    True
    >>> is_anagram("rat", "car")
    False
    >>> is_anagram("a", "ab")
    False
    """
    sfreq = Counter(s)
    tfreq = Counter(t)
    if len(sfreq) != len(tfreq):
        return False
    for chr, cnt in sfreq.items():
        if chr not in tfreq or tfreq[chr] != cnt:
            return False
    return True


# https://leetcode.com/problems/valid-palindrome/
def is_palindrome(s: str) -> bool:
    """
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("race a car")
    False
    >>> is_palindrome(" ")
    True
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if left >= right:
            return True
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
def max_profit(prices: list[int]) -> int:
    """
    >>> max_profit([7, 1, 5, 3, 6, 4])
    5
    >>> max_profit([7, 6, 4, 3, 1])
    0
    """
    min_price_so_far = prices[0]
    max_profit = 0
    for price in prices[1:]:
        if price < min_price_so_far:
            min_price_so_far = price
        elif (profit := price - min_price_so_far) > max_profit:
            max_profit = profit
    return max_profit


# https://leetcode.com/problems/merge-two-sorted-lists/
def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    """
    >>> ListNode.to_list(merge_two_lists(ListNode.from_list([1, 2, 4]), ListNode.from_list([1, 3, 4])))
    [1, 1, 2, 3, 4, 4]
    >>> ListNode.to_list(merge_two_lists(ListNode.from_list([]), ListNode.from_list([])))
    []
    >>> ListNode.to_list(merge_two_lists(ListNode.from_list([]), ListNode.from_list([0])))
    [0]
    """
    ptr = dummy = ListNode()
    while list1 is not None and list2 is not None:
        if list1.val < list2.val:
            ptr.next = ListNode(list1.val)
            list1 = list1.next
        else:
            ptr.next = ListNode(list2.val)
            list2 = list2.next
        ptr = ptr.next
    if list1 is not None:
        ptr.next = list1
    else:
        ptr.next = list2
    return dummy.next


# https://leetcode.com/problems/valid-parentheses/
def is_valid(s: str) -> bool:
    """
    >>> is_valid("()")
    True
    >>> is_valid("()[]{}")
    True
    >>> is_valid("(]")
    False
    >>> is_valid("([])")
    True
    >>> is_valid("([)]")
    False
    """
    bkt = {")": "(", "}": "{", "]": "["}
    stack: list[str] = []
    for c in s:
        if c not in bkt:
            stack.append(c)
            continue
        if len(stack) == 0 or stack[-1] != bkt[c]:
            return False
        stack.pop()
    return len(stack) == 0


# https://leetcode.com/problems/two-sum/
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    >>> two_sum([2, 7, 11, 15], 9)
    [0, 1]
    >>> two_sum([3, 2, 4], 6)
    [1, 2]
    >>> two_sum([3, 3], 6)
    [0, 1]
    """
    indices: dict[int, int] = {}
    for i, n in enumerate(nums):
        needed = target - n
        if needed in indices:
            return [indices[needed], i]
        indices[n] = i
    raise RuntimeError("no solution found")
