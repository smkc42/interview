from collections import deque


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
