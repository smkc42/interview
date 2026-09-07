from __future__ import annotations


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
