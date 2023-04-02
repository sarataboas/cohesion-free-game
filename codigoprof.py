import pygame
import random
import time
import sys
import numpy as np
from copy import deepcopy

NUM_ROWS = 6
NUM_COLS = 7

# RGB codes
PLAYER_1_COLOR = (255, 0, 0)  # red
PLAYER_2_COLOR = (255, 255, 0)  # yellow
EMPTY_CELL_COLOR = (255, 255, 255)  # white
BOARD_COLOR = (0, 0, 255)  # blue

CELL_SIZE = 100
WIDTH = NUM_COLS * CELL_SIZE
HEIGHT = (NUM_ROWS + 1) * CELL_SIZE


class State:
    def _init_(self):
        self.board = np.zeros((NUM_ROWS, NUM_COLS), dtype=int)  # empty board
        # array([[0., 0., 0., 0., 0., 0., 0.],  <- row 0
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 1
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 2
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 3
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 4
        #        [0., 0., 0., 0., 0., 0., 0.]]) <- row 5
        self.column_heights = np.full(NUM_COLS, NUM_ROWS - 1, dtype=int)  # starting from the bottom, row 5
        # array([5, 5, 5, 5, 5, 5])
        self.available_moves = list(range(NUM_COLS))  # can play in any column
        # [0, 1, 2, 3, 4, 5, 6]
        self.player = 1  # player 1 starts
        self.winner = -1  # no winner

    def move(self, column):  # play in a column, e.g., 2
        height = self.column_heights[column]  # e.g., first move in column -> height = 5
        self.board[height][column] = self.player  # update board
        # array([[0., 0., 0., 0., 0., 0., 0.],  <- row 0
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 1
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 2
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 3
        #        [0., 0., 0., 0., 0., 0., 0.],  <- row 4
        #        [0., 0., >1.<, 0., 0., 0., 0.]]) <- row 5

        if height == 0:
            self.available_moves.remove(column)  # e.g., when 2 is filled, [0, 1, 2, 3, 4, 5, 6] -> [0, 1, 3, 4, 5, 6]
        else:
            self.column_heights[
                column] = height - 1  # e.g., after playing in 2 for the first time, array([5, 5, 4, 5, 5, 5])

        self.update_winner()  # check if someone won
        if self.player == 1:  # update player turn
            self.player = 2
        else:
            self.player = 1

        return self  # not saving states -> consider saving them using deepcopy

    def update_winner(self):
        if self.count_lines(4, 1) > 0:  # player 1 has 4 connected pieces
            self.winner = 1  # player 1 wins
        elif self.count_lines(4, 2) > 0:  # player 2 has 4 connected pieces
            self.winner = 2  # player 2 wins
        elif len(self.available_moves) == 0:
            self.winner = 0  # draw

    def count_lines(self, n, player):
        num_lines = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLS):
                if col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row][col], self.board[row][col + 1],
                                                                      self.board[row][col + 2],
                                                                      self.board[row][col + 3]]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and self.check_line(n, player, [self.board[row][col], self.board[row + 1][col],
                                                                      self.board[row + 2][col],
                                                                      self.board[row + 3][col]]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and col < NUM_COLS - 3 and self.check_line(n, player, [self.board[row][col],
                                                                                             self.board[row + 1][
                                                                                                 col + 1],
                                                                                             self.board[row + 2][
                                                                                                 col + 2],
                                                                                             self.board[row + 3][
                                                                                                 col + 3]]):
                    num_lines += 1
                if row < NUM_ROWS - 3 and col > 3 and self.check_line(n, player, [self.board[row][col],
                                                                                  self.board[row + 1][col - 1],
                                                                                  self.board[row + 2][col - 2],
                                                                                  self.board[row + 3][col - 3]]):
                    num_lines += 1
        return num_lines

    # this functions is used to
    #  1. Check if a player has won -> if check_line(4, player, values) > 0
    #  2. Compute heuristics -> check how many lines have 3 connected pieces
    #      i.e., it is good to have (many) lines with 3 pieces, since its close to having 4
    def check_line(self, n, player, values):  # checks if the line has 3 or 4 pieces connected for a given player
        num_pieces = sum(list(map(lambda val: val == player, values)))
        if n == 4:
            return num_pieces == 4
        if n == 3:
            num_empty_spaces = sum(list(map(lambda val: val == 0, values)))
            return num_pieces == 3 and num_empty_spaces == 1

    # this function is used for heuristics, i.e., it is good to have pieces in the center
    def central(self, player):
        points = 0
        for row in range(NUM_ROWS):
            points += 2 * (self.board[row][3] == player)  # center column
            points += (self.board[row][2] == player) + (self.board[row][4] == player)  # around center column
        return points