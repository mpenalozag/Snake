import random
from collections import deque
from threading import Thread
from time import sleep
from curtsies import Input
from os import system
from methods import lost_game

class Game:
    def __init__(self):
        #SETTINGS
        self.x_size = 20
        self.y_size = 40
        self.score = 0
        self.coordinates = dict()
        self.set_coords()        
        self.key_pressed = "'d'"

        #GAME
        self.lost = False

        #SNAKE 
        self.snake = "🟩"
        self.snake_body = deque()
        self.snake_xy = (self.x_size//2, self.y_size//2)

        #FOOD
        self.food = "🟥"
        self.food_xy = None
        self.food_eaten = True

        #THREADS
        self.game_thread = Thread(target=self.game_run)
        self.move_thread = Thread(target=self.move_snake)

    def set_coords(self):
        for x in range(1, self.x_size + 1):
            for y in range(1, self.y_size + 1):
                if x == self.x_size or x == 1 or y == 1:
                    self.coordinates[(x,y)] = "* "
                elif y == self.y_size:
                    self.coordinates[(x,y)] = "*"
                else:
                    self.coordinates[(x,y)] = "  "

    def display_board(self):
        self.display_score()
        self.display_snake()
        self.display_map()
        self.generate_food()

    def update_board(self):
        self.display_score()
        self.display_map()
        
    def display_score(self):
        print(f"SCORE: {self.score}                       S N A K E        ")

    def display_map(self):
        for x in range(1, self.x_size + 1):
            row = ""
            for y in range(1, self.y_size + 1):
                row += self.coordinates[(x,y)]
            print(row)

    def display_snake(self):
        self.coordinates[(self.x_size//2, self.y_size//2)] = self.snake
        self.snake_body.append((self.x_size//2, self.y_size//2))

    def game_run(self):
        self.display_board()
        while not self.lost:
            sleep(0.1)
            system("clear")
            self.update_board()
            self.check_move()
            self.check_limits()
        
    def move_snake(self):
        with Input(keynames='curses') as input_generator:
            for e in input_generator:
                self.key_pressed = repr(e)

    def check_move(self):
        if self.key_pressed == "'a'":
            self.move_snake_body('left')
        if self.key_pressed == "'d'":
            self.move_snake_body('right')
        if self.key_pressed == "'w'":
            self.move_snake_body('up')
        if self.key_pressed == "'s'":
            self.move_snake_body('down')

    def move_snake_body(self, change):
        self.coordinates[self.snake_body[0]] = "  "
        for position in range(len(self.snake_body) - 1):
            self.snake_body[position] = self.snake_body[position + 1]
            self.coordinates[position] = self.snake
        position_x = self.snake_body[-1][0]
        position_y = self.snake_body[-1][1]
        if change == 'left':
            self.snake_body[-1] = (position_x, position_y - 1)
            self.coordinates[(position_x, position_y - 1)] = self.snake
        elif change == 'right':
            self.snake_body[-1] = (position_x, position_y + 1)
            self.coordinates[(position_x, position_y + 1)] = self.snake
        elif change == 'up':
            self.snake_body[-1] = (position_x - 1, position_y)
            self.coordinates[(position_x - 1, position_y)] = self.snake
        elif change == 'down':
            self.snake_body[-1] = (position_x + 1, position_y)
            self.coordinates[(position_x + 1, position_y)] = self.snake
        

    def start_game(self):
        self.game_thread.start()
        self.move_thread.start()

    def generate_food(self):
        x = random.randint(2, self.x_size - 1)
        y = random.randint(2, self.y_size - 1)
        while (x,y) in self.snake_body:
            x = random.randint(2, self.x_size - 1)
            y = random.randint(2, self.y_size - 1)
        self.coordinates[(x,y)] = self.food
        self.food_xy = (x,y)

    def check_limits(self):
        if self.snake_body[-1][0] == 1 or self.snake_body[-1][0] == self.x_size:
            lost_game()
            self.lost = True
        if self.snake_body[-1][1] == 1 or self.snake_body[-1][1] == self.y_size:
            lost_game()
            self.lost = True
        if self.snake_body[-1] == self.food_xy:
            self.append_body_snake(self.food_xy)
            self.generate_food()
            self.score += 1

    def append_body_snake(self, position):
        if self.key_pressed == "'a'":
            self.snake_body.appendleft((position[0], position[1] + len(self.snake_body)))
        if self.key_pressed == "'d'":
            self.snake_body.appendleft((position[0], position[1] - len(self.snake_body)))
        if self.key_pressed == "'w'":
            self.snake_body.appendleft((position[0] + len(self.snake_body), position[1]))
        if self.key_pressed == "'s'":
            self.snake_body.appendleft((position[0] - len(self.snake_body), position[1]))


    



if __name__ == '__main__':
    my_game = Game()
    my_game.start_game()