import time
import random

import keyboard

import led_colors
from settings import ROWS, COLUMNS
from utils import LedMatrixApp, display_text


class Player(LedMatrixApp):

    def __init__(self, up, down, is_last=False):
        keyboard.on_press_key(up, self.go_up)
        keyboard.on_press_key(down, self.go_down)
    
        self.y_pos = 0
        self.x_pos = 15 if is_last else 0

    def go_up(self, up):
        if self.y_pos > 0:
            self.y_pos -= 1
    
    def go_down(self, down):
        if self.y_pos < 13:
            self.y_pos += 1


class Ball(object):

    def __init__(self):
        self.x_pos = 2
        self.y_pos = random.randrange(0, ROWS-1)
        self.x_direction = 1
        self.y_direction = 1
    
    def move(self, board):
        # Top and bottom walls
        if self.y_pos == 0 or self.y_pos == ROWS - 1:
            self.y_direction *= -1

        # Stopping condition
        next_x_pos = self.x_pos + self.x_direction
        next_y_pos = self.y_pos + self.y_direction
        if next_x_pos == 0 or next_x_pos == ROWS - 1:
            if board[next_y_pos][next_x_pos] != 'B':
                print(next_y_pos, next_x_pos)
                print(board[next_y_pos][next_x_pos])
                print(board[next_x_pos][next_y_pos])
                return False
            else:
                self.x_direction *= -1
    
        self.y_pos += self.y_direction
        self.x_pos += self.x_direction

        return True

class Pong(LedMatrixApp):

    display_text = 'PONG'

    def __init__(self): 
        self.player1 = Player('q', 'a')
        self.player2 = Player('p', 'l', is_last=True)

        self.ball = Ball()

        self.wait = 0.3

        self.matrix = [[0 for i in range(16)] for j in range(16)]

    def render_board(self):
        for i in range(ROWS):
            for j in range(COLUMNS):
                character = ' '
                if i == self.ball.y_pos and j == self.ball.x_pos:
                    character = 'O'

                self.matrix[i][j] = character

        def render_player_on_board(board, player):
            for i in range(3):
                board[player.y_pos+i][player.x_pos] = 'B'

        for p in (self.player1, self.player2):
            render_player_on_board(self.matrix, p)

    def end(self):
        display_text(
            "PLAYER {} WON!".format(int(self.ball.x_pos == 0) + 1))

    def play(self):
        time_since_last_ball_update = 0

        while True:
            time.sleep(self.wait / 5)
            time_since_last_ball_update += self.wait / 5

            self.render_board()

            if time_since_last_ball_update >= self.wait:
                time_since_last_ball_update = 0
                if not self.ball.move(self.matrix):
                    self.end()
                    return
                self.wait -= self.wait / 1000

            # Production
            # self.show(self.get_colored_matrix(self.matrix))

            # Development
            self.show(self.matrix)