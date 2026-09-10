from __future__ import annotations

from collections import deque


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, arr: list[int]) -> ListNode | None:
        if len(arr) == 0:
            return None
        ptr = dummy = cls()
        for it in arr:
            ptr.next = cls(it)
            ptr = ptr.next
        return dummy.next

    @classmethod
    def to_list(cls, lst: ListNode | None) -> list[int]:
        if lst is None:
            return []
        ret: list[int] = []
        while lst is not None:
            ret.append(lst.val)
            lst = lst.next
        return ret


class TreeNode:
    def __init__(
        self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_list(cls, arr: list[int | None]) -> TreeNode | None:
        if len(arr) == 0 or arr[0] is None:
            return None
        root = cls(arr[0])
        q = deque([root])
        ptr = 0
        while len(q) > 0:
            node = q.popleft()
            ptr += 1
            if ptr == len(arr):
                break
            if (x := arr[ptr]) is not None:
                node.left = cls(x)
                q.append(node.left)
            ptr += 1
            if ptr == len(arr):
                break
            if (x := arr[ptr]) is not None:
                node.right = cls(x)
                q.append(node.right)
        return root

    @classmethod
    def to_list(cls, root: TreeNode | None) -> list[int | None]:
        if root is None:
            return []
        ret: list[int | None] = [root.val]
        q = deque([root])
        while len(q) > 0:
            node = q.popleft()
            if node.left is not None:
                ret.append(node.left.val)
                q.append(node.left)
            else:
                ret.append(None)
            if node.right is not None:
                ret.append(node.right.val)
                q.append(node.right)
            else:
                ret.append(None)
        while len(ret) > 0 and ret[-1] is None:
            ret.pop()
        return ret
