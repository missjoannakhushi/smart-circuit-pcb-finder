class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Push an item onto the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        """Check whether the stack is empty."""
        return len(self.items) == 0

    def size(self):
        """Return stack size."""
        return len(self.items)


def in_bounds(row, col, board):
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_neighbors(row, col):
    """Return up/down/left/right neighbor coordinates."""
    return [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)
    ]


def find_short_circuit(board, start=(0, 0)):
    """
    Performs a DFS traversal using an explicit LIFO stack.
    Returns:
    {
        "short_detected": bool,
        "position": (row, col) or None,
        "path": list of visited coordinates,
        "visited_count": int
    }
    """

    if not board or not board[0]:
        return {
            "short_detected": False,
            "position": None,
            "path": [],
            "visited_count": 0
        }

    stack = Stack()
    visited = set()
    path = []

    start_row, start_col = start
    if not in_bounds(start_row, start_col, board):
        raise ValueError("Start position is out of bounds.")

    stack.push(start)
    visited.add(start)

    while not stack.is_empty():
        current = stack.pop()
        path.append(current)

        row, col = current

        if not in_bounds(row, col, board):
            continue

        # If the cell is a short-circuit node, immediately flag it
        if board[row][col] == 2:
            return {
                "short_detected": True,
                "position": (row, col),
                "path": path,
                "visited_count": len(visited)
            }

        # Explore valid copper neighbors (1 or 2)
        for nr, nc in get_neighbors(row, col):
            if in_bounds(nr, nc, board):
                cell_value = board[nr][nc]
                if cell_value in (1, 2) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.push((nr, nc))

    return {
        "short_detected": False,
        "position": None,
        "path": path,
        "visited_count": len(visited)
    }
