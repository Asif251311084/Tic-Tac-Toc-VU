
# TIC TAC TOE AI
# Minimax + DFS + Alpha-Beta Pruning

board = []

player_mark = 'X'
computer_mark = 'O'


# Set Player and Computer Marks
def setMarks(mark):

    global player_mark, computer_mark

    player_mark = mark

    if mark == 'X':
        computer_mark = 'O'
    else:
        computer_mark = 'X'

    resetBoard()


# Reset Board
def resetBoard():

    global board

    board = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9']
    ]


# Check Empty Cells
def isMovesLeft():

    for i in range(3):
        for j in range(3):

            if board[i][j] in '123456789':
                return True

    return False


# Evaluate Board
def evaluate():

    lines = []

    # Rows
    for i in range(3):
        lines.append(board[i])

    # Columns
    for j in range(3):
        lines.append([
            board[0][j],
            board[1][j],
            board[2][j]
        ])

    # Diagonals
    lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])

    lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])

    for line in lines:

        if line[0] == line[1] == line[2]:

            if line[0] == computer_mark:
                return 10

            if line[0] == player_mark:
                return -10

    return 0


# Minimax + DFS + Alpha-Beta
def minimax(isMax, depth, alpha, beta):

    score = evaluate()

    if score == 10:
        return score - depth

    if score == -10:
        return score + depth

    if not isMovesLeft():
        return 0

    # Computer Turn
    if isMax:

        best = -1000

        for i in range(3):
            for j in range(3):

                if board[i][j] in '123456789':

                    temp = board[i][j]

                    board[i][j] = computer_mark

                    best = max(
                        best,
                        minimax(False, depth + 1, alpha, beta)
                    )

                    board[i][j] = temp

                    alpha = max(alpha, best)

                    if beta <= alpha:
                        return best

        return best

    # Player Turn
    else:

        best = 1000

        for i in range(3):
            for j in range(3):

                if board[i][j] in '123456789':

                    temp = board[i][j]

                    board[i][j] = player_mark

                    best = min(
                        best,
                        minimax(True, depth + 1, alpha, beta)
                    )

                    board[i][j] = temp

                    beta = min(beta, best)

                    if beta <= alpha:
                        return best

        return best


# Computer Best Move
def computerMove():

    bestValue = -1000

    bestRow = -1
    bestCol = -1

    alpha = -1000
    beta = 1000

    for i in range(3):
        for j in range(3):

            if board[i][j] in '123456789':

                temp = board[i][j]

                board[i][j] = computer_mark

                moveValue = minimax(
                    False, 1, alpha, beta
                )

                board[i][j] = temp

                if moveValue > bestValue:

                    bestValue = moveValue

                    bestRow = i
                    bestCol = j

                alpha = max(alpha, bestValue)

    if bestRow != -1:

        board[bestRow][bestCol] = computer_mark

    return bestRow, bestCol


# Initialize Board
resetBoard()
