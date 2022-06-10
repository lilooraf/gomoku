import os
import math
import sys

class Game:

    board = []
    turn = False

    empty = -1
    player1 = 0
    player2 = 1
    
    def __init__(self, rules, size):
        self.rules = rules
        self.size = size
        self.initBoard()

    def displayBoard(self, board):
        print("    ", end='')
        for x_axe in range(0, self.size):
            if (x_axe >= 10):
                print(x_axe, end="  ")
            else:
                print(x_axe, end="   ")
        print("X\n")
        y_axe = 0
        for y in board:
            if (y_axe >= 10):
                print(y_axe, end="  ")
            else:
                print(y_axe, end="   ")
            y_axe += 1
            for x in y:
                if (x == 0):
                    print("O", end="   ")
                elif (x == 1):
                    print("X", end="   ")
                elif (x == -1):
                    print("-", end="   ")
                else:
                    print(x, end="   ")
            print("\n")
        print("Y")

    def play(self, x, y):
        for i in range(self.size):
            if i == y - 1:
                for j in range(self.size):
                    if j == x - 1:
                        if self.board[i][j] != -1:
                            return 84
                        self.board[i][j] = int(self.turn)
                        self.turn = not self.turn
                        return 0

    def checkWin(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                (point1, end, check) = self.checkSuiteHorizontal(y, x, self.board[y][x])
                (point2, end, check) = self.checkSuiteVertical(y, x, self.board[y][x])
                (point3, end, check) = self.checkSuiteDiagnalDown(y, x, self.board[y][x])
                (point4, end, check) = self.checkSuiteDiagnalUp(y, x, self.board[y][x])
                if (max(point1, point2, point3, point4) >= self.rules.suiteForWin):
                    return (1, self.board[y][x])
        return (0, 0)

    def notationLine(self, point, end):
        if (point >= 5):
            return point * 1000
        if (point == 1 or end == 2):
            return point / 4
        if (point == 3 and end == 0):
            return point * 2
        if (point == 4 and end == 0):
            return point * 100
        if (point == 4 and end == 1):
            return point * 100
        return point

    def checkBiggestSuite(self, y, x, player):
        (point, end, check1) = self.checkSuiteHorizontal(y, x, player)
        h = self.notationLine(point, end)
        (point, end, check2) = self.checkSuiteVertical(y, x, player)
        v = self.notationLine(point, end)
        (point, end, check3) = self.checkSuiteDiagnalDown(y, x, player)
        dd = self.notationLine(point, end)
        (point, end, check4) = self.checkSuiteDiagnalUp(y, x, player)
        du = self.notationLine(point, end)
        check = check1 + check2 + check3 + check4
        return ((h + v + dd + du), check)

    def checkSuiteHorizontal(self, y, x, player):
        check = []
        end = 0
        n = 1
        for i in range(x - 1, x - self.rules.suiteForWin):
            if i < 0 or i >= self.size:
                break
            elif self.board[y][i] == player:
                check.append([y, i])
                n += 1
            elif self.board[y][i] != self.empty:
                end += 1
                break
            else:
                break
        for i in range(x + 1, x + self.rules.suiteForWin):
            if i < 0 or i >= self.size:
                break
            elif self.board[y][i] == player:
                check.append([y, i])
                n += 1
            elif self.board[y][i] != self.empty:
                end += 1
                break
            else:
                break
        return (n, end, check)

    def checkSuiteVertical(self, y, x, player):
        check = []
        end = 0
        n = 1
        for i in range(y - 1, y - self.rules.suiteForWin):
            if i < 0 or i >= self.size:
                break
            elif self.board[i][x] == player:
                check.append([i, x])
                n += 1
            elif self.board[i][x] != self.empty:
                end += 1
                break
            else:
                break
        for i in range(y + 1, y + self.rules.suiteForWin):
            if i < 0 or i >= self.size:
                break
            elif self.board[i][x] == player:
                check.append([i, x])
                n += 1
            elif self.board[i][x] != self.empty:
                end += 1
                break
            else:
                break
        return (n, end, check)
    
    def checkSuiteDiagnalDown(self, y, x, player):
        check = []
        end = 0
        n = 1
        for i in range(1, self.rules.suiteForWin):
            if y - i < 0 or y - i >= self.size or x - i < 0 or x - i >= self.size:
                break
            elif self.board[y - i][x - i] == player:
                check.append([y - i, x - i])
                n += 1
            elif self.board[y - i][x - i] != self.empty:
                end += 1
                break
            else:
                break
        for i in range(1, self.rules.suiteForWin):
            if y + i < 0 or y + i >= self.size or x + i < 0 or x + i >= self.size:
                break
            elif self.board[y + i][x + i] == player:
                check.append([y + i, x + i])
                n += 1
            elif self.board[y + i][x + i] != self.empty:
                end += 1
                break
            else:
                break
        return (n, end, check)

    def checkSuiteDiagnalUp(self, y, x, player):
        check = []
        end = 0
        n = 1
        for i in range(1, self.rules.suiteForWin):
            if y + i < 0 or y + i >= self.size or x - i < 0 or x - i >= self.size:
                break
            elif self.board[y + i][x - i] == player:
                check.append([y + i, x - i])
                n += 1
            elif self.board[y + i][x - i] != self.empty:
                end += 1
                break
            else:
                break
        for i in range(1, self.rules.suiteForWin):
            if y - i < 0 or y - i >= self.size or x + i < 0 or x + i >= self.size:
                break
            elif self.board[y - i][x + i] == player:
                check.append([y - i, x + i])
                n += 1
            elif self.board[y - i][x + i] != self.empty:
                end += 1
                break
            else:
                break
        return (n, end, check)

    def initBoard(self):
        for i in range(self.size):
            self.board.append([])
            for j in range (self.size):
                self.board[i].append(-1)
                j = j
    
    def allPossibleMoves(self, board):
        allMoves = []
        allfinalMoves = []
        for y in range(0, self.size):
            for x in range(0, self.size):
                if board[y][x] != -1:
                    allMoves.append([y - 1, x + 1])
                    allMoves.append([y - 1, x])
                    allMoves.append([y - 1, x - 1])
                    allMoves.append([y + 1, x + 1])
                    allMoves.append([y + 1, x])
                    allMoves.append([y + 1, x - 1])
                    allMoves.append([y, x + 1])
                    allMoves.append([y, x - 1])
        for move in allMoves:
            if move[0] < 0 or move[0] >= self.size or move[1] < 0 or move[1] >= self.size:
                continue
            if (board[move[0]][move[1]] == -1):
                allfinalMoves.append([move[0], move[1]])
        return allfinalMoves

    def getBoardSize(self):
        return self.size