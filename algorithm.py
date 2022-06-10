import math
import sys

class Algorithm:
    boardSave = []

    def __init__(self, game, rules):
        self.game = game
        self.rules = rules

    def isAlreadyCheck(self, check, y, x):
        for a in check:
            if (a[0] == y and a[1] == x):
                return True
        return False

    def evaluateBoard(self, board, player):
        check = []
        resMax = 0
        resMin = 0
        notPlayer = 0 if player == 1 else 1
        for y in range(0, self.game.size):
            for x in range(0, self.game.size):
                if (self.isAlreadyCheck(check, y, x) == False and board[y][x] == player):
                    (resTmp, checkTmp) = self.game.checkBiggestSuite(y, x, player)
                    resMax += resTmp
                    check = check + checkTmp
                elif board[y][x] == notPlayer:
                    (resTmp, checkTmp) = self.game.checkBiggestSuite(y, x, notPlayer)
                    resMin += resTmp
                    check = check + checkTmp
        return resMax - resMin
    
    def play(self, board):
        self.game.board = board
        self.game.displayBoard(self.game.board)

        while 1:
            board = self.game.board
            print("Eval Board:" + str(self.evaluateBoard(self.game.board, 0)))
            usr_x = input("Enter your X: ")
            usr_y = input("Enter your Y: ")
            self.game.board[int(usr_y)][int(usr_x)] = 1
            self.game.displayBoard(self.game.board)
            moves = self.game.allPossibleMoves(self.game.board)
            res = self.minimax(moves, self.rules.depth, -math.inf, math.inf, True, board)
            self.game.board[res[1][0]][res[1][1]] = 0
            self.game.displayBoard(self.game.board)

    def minimax(self, positions, depth, alpha, beta, maximizingPlayer, board):
        if depth == 0:
            return [self.evaluateBoard(board, 0), 0]

        if maximizingPlayer:
            maxEval = [-math.inf, []]
            for move in positions:
                board[move[0]][move[1]] = 0
                evalu = self.minimax(self.game.allPossibleMoves(board), depth - 1, alpha, beta, False, board)
                board[move[0]][move[1]] = -1
                if maxEval[0] < evalu[0]:
                    maxEval[0] = evalu[0]
                    maxEval[1] = move
                alpha = max(alpha, evalu[0])
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = [math.inf, []]
            for move in positions:
                board[move[0]][move[1]] = 1
                evalu = self.minimax(self.game.allPossibleMoves(board), depth - 1, alpha, beta, True, board)
                board[move[0]][move[1]] = -1
                if minEval[0] > evalu[0]:
                    minEval[0] = evalu[0]
                    minEval[1] = move
                beta = min(beta, evalu[0])
                if beta <= alpha:
                    break
            return minEval