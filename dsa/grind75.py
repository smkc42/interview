from datastructures import ListNode


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
