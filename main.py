import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text, CommonCases

from consts import *

class SlowFruit(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/apple.gif', x, y)

        self.app = app
        self.name = 'SlowFruit'

    def update(self):
        self.y += FRUIT_SLOW_SPEED

        super().outofcanvas()


class FastFruit(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/banana.gif', x, y)

        self.app = app
        self.name = 'FastFruit'

    def update(self):
        self.y += FRUIT_FAST_SPEED

        super().outofcanvas()


class SlideFruit(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/cherry.gif', x, y)

        self.app = app
        self.direction = randint(0,1)*2 - 1
        self.name = 'SlideFruit'

    def update(self):
        self.y += FRUIT_FAST_SPEED
        self.x += self.direction * 5

        super().outofcanvas()


class CurvyFruit(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/pear.gif', x, y)

        self.app = app
        self.t = randint(0,360) * 2 * math.pi / 360
        self.name = 'CurvyFruit'

    def update(self):
        self.y += FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.x += math.sin(self.t*0.08)*10

        super().outofcanvas()

class Basket(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/basket.gif', x, y)

        self.app = app
        self.direction = None

    def update(self):
        if self.direction == BASKET_LEFT:
            if self.x >= BASKET_MARGIN:
                self.x -= BASKET_SPEED
        elif self.direction == BASKET_RIGHT:
            if self.x <= CANVAS_WIDTH - BASKET_MARGIN:
                self.x += BASKET_SPEED

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= BASKET_CATCH_DISTANCE:
            fruit.to_be_deleted = True
            if fruit.name == 'CurvyFruit':
                self.app.score += 4
            elif fruit.name == 'SlideFruit':
                self.app.score += 3
            elif fruit.name == 'FastFruit':
                self.app.score += 2
            else:
                self.app.score += 1
            self.app.update_score()


class BasketGame(GameApp):
    def init_game(self):
        self.basket = Basket(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.elements.append(self.basket)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            x = randint(50, CANVAS_WIDTH - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(self, x, 0)
            elif p <= 0.6:
                new_fruit = FastFruit(self, x, 0)
            elif p <= 0.8:
                new_fruit = SlideFruit(self, x, 0)
            else:
                new_fruit = CurvyFruit(self, x, 0)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.basket.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        if event.keysym == 'Left':
            self.basket.direction = BASKET_LEFT
        elif event.keysym == 'Right':
            self.basket.direction = BASKET_RIGHT
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Basket Fighter")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = BasketGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
