from collections import Counter, defaultdict

        
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
