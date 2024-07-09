# player.py

STARTING_HEALTH = 100
STARTING_AMMO = 5
HEALTH_PACK_HEAL = 20
GRID_SIZE = 15

class Player:
    def __init__(self, name):
        self.name = name
        self.health = STARTING_HEALTH
        self.ammo = STARTING_AMMO
        self.position = (0, 0)
        self.inventory = []

    def move(self, direction):
        x, y = self.position
        if direction == 'north' and y > 0:
            y -= 1
        elif direction == 'south' and y < GRID_SIZE - 1:
            y += 1
        elif direction == 'east' and x < GRID_SIZE - 1:
            x += 1
        elif direction == 'west' and x > 0:
            x -= 1
        self.position = (x, y)

    def attack(self, zombies, direction):
        if self.ammo > 0:
            self.ammo -= 1
            x, y = self.position
            if direction == 'north':
                target_pos = (x, y - 1)
            elif direction == 'south':
                target_pos = (x, y + 1)
            elif direction == 'east':
                target_pos = (x + 1, y)
            elif direction == 'west':
                target_pos = (x - 1, y)
            else:
                return None
            
            # Check if the target position has a zombie
            for zombie in zombies:
                zx, zy = zombie.position
                if (zx, zy) == target_pos:
                    return zombie
        return None

    def heal(self):
        if 'health_pack' in self.inventory:
            self.inventory.remove('health_pack')
            self.health += HEALTH_PACK_HEAL
