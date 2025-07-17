
def check(row, col, num, puzzle_sol):
    for i in range(9):
        if puzzle_sol[row][i] == num:
            return False
    for i in range(9):
        if puzzle_sol[i][col] == num:
            return False
    row = row - row % 3
    col = col - col % 3
    for i in range(3):
        for j in range(3):
            if puzzle_sol[row + i][col + j] == num:
                return False
    return True

def iterate_puzzle(puzzle_sol):
    for row in range(9):
        for col in range(9):
            if (puzzle_sol[row][col] == 0):
                for i in range(1, 10):
                    if (check(row, col, i, puzzle_sol)):
                        puzzle_sol[row][col] = i
                        if iterate_puzzle(puzzle_sol): return True
                        puzzle_sol[row][col] = 0
                return False
    return True


def generateCandidates(puzzle):
    candidates = [[[] for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                for k in range(1, 10):
                    if (check(i, j, k, puzzle)):
                        candidates[i][j].append(k)


    hint = checkNakedCell(candidates)

    if hint is not None:
        return hint


def checkNakedCell(candidates):
    for i in range(9):
        for j in range(9):
            if len(candidates[i][j]) == 1:
                return (i, j, candidates[i][j][0], "NS")
    return None
            







               