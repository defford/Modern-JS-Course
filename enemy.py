# enemy.py

import random

GRID_SIZE = 15

class Zombie:
    def __init__(self, position):
        self.position = position

    def move_towards(self, target_position):
        x, y = self.position
        tx, ty = target_position
        if x != tx and (y == ty or random.choice([True, False])):
            x += 1 if tx > x else -1
        elif y != ty:
            y += 1 if ty > y else -1
        self.position = (x, y)

def place_zombies(num_zombies):
    zombies = []
    for _ in range(num_zombies):
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        zombies.append(Zombie(pos))
    return zombies
