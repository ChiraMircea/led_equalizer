import copy
import time
import random
from contextlib import suppress

import keyboard

import led_colors
from utils import LedMatrixApp, display_text
from settings import ROWS, COLUMNS


class Snake(LedMatrixApp):

    display_text = 'SNEK'

    def __init__(self):
        for key in ['w', 'a', 's', 'd']:
            keyboard.on_press_key(key, self.set_direction)

        self.wait = 1
        self.direction = 'w'
        self.body = [(0, 0),(0, 1),(0, 2)]

        self.allow_move = True

        self.matrix = [[0 for i in range(ROWS)] for j in range(COLUMNS)]

        self.render_snake()
        self.generate_food()
    
    def set_direction(self, keyboard_event):
        if self.allow_move is False:
            return

        oposites = {
            'w': 's',
            's': 'w',
            'a': 'd',
            'd': 'a'
        }
            
        if oposites[keyboard_event.name] != self.direction:
            self.direction = keyboard_event.name
            self.allow_move = False

    def get_location(self, location):
        return self.matrix[location[0]][location[1]]

    def move(self, direction):
        next_move = self.check_move(self.get_next_move(direction))

        self.body.append(next_move)
        
        if self.get_location(next_move) == 'F':
            self.wait = self.wait - (self.wait / len(self.body))
            self.generate_food()
        else:
            self.body = self.body[1:]

        # Stopping condition
        if next_move in self.body[:-1]:
            return False

        self.render_snake()
        self.allow_move = True

        return True
        
    def render_snake(self):
        """Compute the snake's and food's location on the matrix.
        
        This matrix will be colored accordingly but it is filled here with
        characters so that it will be easier to debug (or play in terminal).
        """
        for i in range(ROWS):
            for j in range(COLUMNS):
                if (j, i) in self.body:
                    self.matrix[j][i] = '0'
                elif self.get_location((j, i)) != 'F':
                    self.matrix[j][i] = ' '

    def generate_food(self):
        def get_position():
            return random.randrange(0, ROWS)

        food_location = self.body[-1]

        while food_location in self.body:
            food_location = (get_position(), get_position())

        self.matrix[food_location[0]][food_location[1]] = 'F'

    def get_next_move(self, direction):
        """
        W - up
        S - down
        D - right
        A - left
        """
        last_move = self.body[-1]

        if direction == 'w':
            return (last_move[0] - 1, last_move[1])
        elif direction == 'd':
            return (last_move[0], last_move[1] + 1)
        elif direction == 's':
            return (last_move[0] + 1, last_move[1])
        elif direction == 'a':
            return (last_move[0], last_move[1] - 1)
    
    def check_move(self, move):
        """Ensure that the move is within the matrix."""
        def check(position):
            if position < 0 or position >= ROWS:
                position = abs(position)
                return abs(ROWS - position)
            return position

        return (check(move[0]), check(move[1]))       
 
    def end(self):
        display_text("SCORE:  {}".format(len(self.body)))

    def color(self):
        self.colored_matrix = copy.deepcopy(self.matrix)

        # Color the snake's body starting from BLUE and going a constant step
        # twards GREEN from tail to head
        step = 255.0 / len(self.body)
        for index, segment in enumerate(self.body):
            color = (0, 255 - index * step, index * step)
            self.colored_matrix[segment[0]][segment[1]] = color
        
        # Color the other cells, ignoring the body
        for i in range(ROWS):
            for j in range(COLUMNS):
                if (i, j) in self.body:
                    continue
                
                # The food will also be colored RED
                if self.colored_matrix[i][j] == 'F':
                    color = led_colors.RED
                else:
                    color = led_colors.EMPTY

                self.colored_matrix[i][j] = color

    def play(self):
        while True:
            time.sleep(self.wait)
            if not self.move(self.direction):
                self.end()
                return
            self.color()

            # Production
            # self.show(matrix_output)

            # Development
            self.show(self.matrix)
