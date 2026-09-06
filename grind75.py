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
