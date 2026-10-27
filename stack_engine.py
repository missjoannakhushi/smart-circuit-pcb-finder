def find_short_circuit(board, start=(0, 0)):
    """
    Advanced Stack-based algorithm (DFS) to traverse the entire PCB 
    trace network and isolate ALL short-circuits.
    """
    rows = len(board)
    cols = len(board[0])
    
    stack = []
    visited = set()
    path = []
    found_shorts = []
    
    # Push starting node if it's valid
    if 0 <= start[0] < rows and 0 <= start[1] < cols:
        stack.append(start)
    
    while len(stack) > 0:
        # POP the top node (LIFO behavior)
        curr_r, curr_c = stack.pop()
        
        if (curr_r, curr_c) in visited:
            continue
            
        visited.add((curr_r, curr_c))
        path.append((curr_r, curr_c))
        
        # Check if current node is a short circuit (Value == 2)
        if board[curr_r][curr_c] == 2:
            if (curr_r, curr_c) not in found_shorts:
                found_shorts.append((curr_r, curr_c))
            # We don't break here anymore; we keep scanning the whole net!
            
        # Explore 4-directional neighbors (Up, Down, Left, Right)
        neighbors = [
            (curr_r - 1, curr_c),
            (curr_r + 1, curr_c),
            (curr_r, curr_c - 1),
            (curr_r, curr_c + 1)
        ]
        
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols:
                # If it's copper trace (1) or short node (2) and unvisited
                if board[nr][nc] in (1, 2) and (nr, nc) not in visited:
                    stack.append((nr, nc))
                    
    return {
        "short_detected": len(found_shorts) > 0,
        "positions": found_shorts,  # Returns a list of all detected shorts
        "path": path
    }
