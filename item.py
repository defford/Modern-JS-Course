# item.py

import random

GRID_SIZE = 15
AMMO_SIZE = 3

class Item:
    def __init__(self, item_type, position):
        self.item_type = item_type
        self.position = position

    def apply_effect(self, player, zombies):
        if self.item_type == 'health_potion':
            player.inventory.append('health_pack')
        elif self.item_type == 'power_up':
            for zombie in zombies:
                zx, zy = zombie.position
                px, py = player.position
                if abs(zx - px) <= 1 and abs(zy - py) <= 1:
                    zombies.remove(zombie)
        elif self.item_type == 'ammo':
            player.ammo += AMMO_SIZE  # Add 3 ammo when ammo item is picked up

def spawn_item():
    item_type = random.choice(['health_potion', 'power_up', 'ammo'])
    pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    return Item(item_type, pos)
