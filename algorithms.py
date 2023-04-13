import heapq

def get_successors(board):
    successors = []
    for row in range(4):
        for col in range(4):
            if board[row][col] != 0:
                # Try moving left
                if col > 0 and board[row][col - 1] == 0:
                    new_board = [r[:] for r in board]
                    new_board[row][col - 1] = new_board[row][col]
                    new_board[row][col] = 0
                    successors.append(new_board)

                # Try moving right
                if col < 3 and board[row][col + 1] == 0:
                    new_board = [r[:] for r in board]
                    new_board[row][col + 1] = new_board[row][col]
                    new_board[row][col] = 0
                    successors.append(new_board)

                # Try moving up
                if row > 0 and board[row - 1][col] == 0:
                    new_board = [r[:] for r in board]
                    new_board[row - 1][col] = new_board[row][col]
                    new_board[row][col] = 0
                    successors.append(new_board)

                # Try moving down
                if row < 3 and board[row + 1][col] == 0:
                    new_board = [r[:] for r in board]
                    new_board[row + 1][col] = new_board[row][col]
                    new_board[row][col] = 0
                    successors.append(new_board)
    return successors


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# calculate the total Manhattan distance for the current state
def heuristic(state):
    total_distance = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] != 0:
                final_pos = ((state[i][j]-1) // 4, (state[i][j]-1) % 4)
                total_distance += manhattan_distance((i, j), final_pos)
    return total_distance

def solve_astar(initial_state,h):
    queue = []
    heapq.heappush(queue, (h(initial_state), initial_state, []))
    visited = set()
    while queue:
        _, state, path = heapq.heappop(queue)
        from finalproject import check_win
        if check_win(state):
            return path
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in get_successors(state):
            heapq.heappush(queue, (len(path) + 1 + h(successor), successor, path+[(successor, len(path)+1)]))
    return None


import heapq
def greedy_search(initial_state, h):
    queue = []
    heapq.heappush(queue, (h(initial_state), initial_state, []))
    visited = set()
    while queue:
        _, state, path = heapq.heappop(queue)
        from finalproject import check_win
        if check_win(state):
            return path
        if str(state) in visited:
            continue
        visited.add(str(state))
        for successor in get_successors(state):
            heapq.heappush(queue, (h(successor), successor, path + [(successor, len(path) + 1)]))

    return None

