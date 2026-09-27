import heapq
from collections import Counter, defaultdict, deque

from dsa.datastructures import TreeNode


# https://leetcode.com/problems/majority-element/
def majority_element(nums: list[int]) -> int:
    """
    >>> majority_element([3, 2, 3])
    3
    >>> majority_element([2, 2, 1, 1, 1, 2, 2])
    2
    """
    cnt = Counter(nums)
    for n in cnt:
        if cnt[n] > len(nums) // 2:
            return n
    raise RuntimeError("no majority element found")


# https://leetcode.com/problems/find-median-from-data-stream/
class MedianFinder:
    """
    >>> mf = MedianFinder()
    >>> mf.add_num(1)
    >>> mf.add_num(2)
    >>> mf.median()
    1.5
    >>> mf.add_num(3)
    >>> mf.median()
    2.0
    """

    def __init__(self):
        self.maxh: list[int] = []
        self.minh: list[int] = []

    def add_num(self, num: int) -> None:
        if len(self.maxh) == 0:
            heapq.heappush_max(self.maxh, num)
            return
        left = self.maxh[0]
        if num <= left:
            heapq.heappush_max(self.maxh, num)
        else:
            heapq.heappush(self.minh, num)
        if abs(len(self.maxh) - len(self.minh)) > 1:
            if len(self.maxh) > len(self.minh):
                x = heapq.heappop_max(self.maxh)
                heapq.heappush(self.minh, x)
            else:
                x = heapq.heappop(self.minh)
                heapq.heappush_max(self.maxh, x)

    def median(self) -> float:
        if len(self.maxh) == len(self.minh):
            return (self.maxh[0] + self.minh[0]) / 2
        else:
            return (
                float(self.maxh[0])
                if len(self.maxh) > len(self.minh)
                else float(self.minh[0])
            )


# https://leetcode.com/problems/trapping-rain-water/
def trap(height: list[int]) -> int:
    """
    >>> trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    >>> trap([4, 2, 0, 3, 2, 5])
    9
    """
    left = [height[0]]
    for i in range(1, len(height)):
        left.append(max(left[-1], height[i]))
    right = [height[-1]]
    for i in range(len(height) - 2, -1, -1):
        right.append(max(right[-1], height[i]))
    right.reverse()
    water = 0
    for l, r, h in zip(left, right, height):
        water += max(0, min(l, r) - h)
    return water


# https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
class Codec:
    """
    >>> ser = Codec()
    >>> deser = Codec()
    >>> TreeNode.to_list(deser.deserialize(ser.serialize(TreeNode.from_list([1, 2, 3, None, None, 4, 5]))))
    [1, 2, 3, None, None, 4, 5]
    >>> TreeNode.to_list(deser.deserialize(ser.serialize(TreeNode.from_list([]))))
    []
    """

    def serialize(self, root: TreeNode | None) -> str:
        if root is None:
            return "null"
        q = deque([root])
        ser: list[int | None] = [root.val]
        while len(q) > 0:
            node = q.popleft()
            if node.left is not None:
                q.append(node.left)
                ser.append(node.left.val)
            else:
                ser.append(None)
            if node.right is not None:
                q.append(node.right)
                ser.append(node.right.val)
            else:
                ser.append(None)
        while len(ser) > 0 and ser[-1] is None:
            ser.pop()
        return ",".join([str(i) if i is not None else "null" for i in ser])

    def deserialize(self, data: str) -> TreeNode | None:
        des = [int(i) if i != "null" else None for i in data.split(",")]
        if len(des) == 0 or des[0] is None:
            return None
        root = TreeNode(des[0])
        q = deque([root])
        ptr = 1
        while len(q) > 0:
            node = q.popleft()
            if ptr < len(des):
                if (left := des[ptr]) is not None:
                    node.left = TreeNode(left)
                    q.append(node.left)
                ptr += 1
            if ptr < len(des):
                if (right := des[ptr]) is not None:
                    node.right = TreeNode(right)
                    q.append(node.right)
                ptr += 1
        return root


# https://leetcode.com/problems/minimum-window-substring/
def min_window(s: str, t: str) -> str:
    """
    >>> min_window("ADOBECODEBANC", "ABC")
    'BANC'
    >>> min_window("a", "a")
    'a'
    >>> min_window("a", "aa")
    ''
    """
    tfreq = Counter(t)
    wfreq: dict[str, int] = defaultdict(int)

    def valid() -> bool:
        for c in tfreq:
            if tfreq[c] > wfreq[c]:
                return False
        return True

    start = end = 0
    minw_start = minw_end = -1
    while end < len(s):
        wfreq[s[end]] += 1
        while valid() and start <= end:
            if minw_start == -1 or end - start < minw_end - minw_start:
                minw_start, minw_end = start, end
            wfreq[s[start]] -= 1
            start += 1
        end += 1
    return "" if minw_start == -1 else s[minw_start : minw_end + 1]


# https://leetcode.com/problems/time-based-key-value-store/
class TimeMap:
    """
    >>> tm = TimeMap()
    >>> tm.set("foo", "bar", 1)
    >>> tm.get("foo", 1)
    'bar'
    >>> tm.get("foo", 3)
    'bar'
    >>> tm.set("foo", "bar2", 4)
    >>> tm.get("foo", 4)
    'bar2'
    >>> tm.get("foo", 5)
    'bar2'
    """

    def __init__(self):
        self.map: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.map:
            self.map[key] = []
        self.map[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.map:
            return ""
        stream = self.map[key]
        low, high, boundary = 0, len(stream) - 1, -1
        while low <= high:
            mid = (low + high) // 2
            cur_timestamp, _ = stream[mid]
            if cur_timestamp <= timestamp:
                boundary = mid
                low = mid + 1
            else:
                high = mid - 1
        return "" if boundary == -1 else stream[boundary][1]
