import pygame
import random
import time

# Constants
GRID_SIZE = 15
TILE_SIZE = 100
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
STARTING_HEALTH = 100
STARTING_AMMO = 5
ZOMBIE_DAMAGE = 15
HEALTH_PACK_HEAL = 20
ZOMBIE_MOVE_DELAY = 50  # Zombies move every second tick
ZOMBIE_SPAWN_INTERVAL = 5000  # Spawn a zombie every 5 seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game entities
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

class Item:
    def __init__(self, item_type, position):
        self.item_type = item_type
        self.position = position

    def apply_effect(self, player, zombies):
        if self.item_type == 'health_potion':
            if 'health_pack' not in player.inventory:
                player.inventory.append('health_pack')
        elif self.item_type == 'power_up':
            for zombie in zombies:
                zx, zy = zombie.position
                px, py = player.position
                if abs(zx - px) <= 1 and abs(zy - py) <= 1:
                    zombies.remove(zombie)
            return None
            pass

def generate_grid():
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def place_zombies(num_zombies):
    zombies = []
    for _ in range(num_zombies):
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        zombies.append(Zombie(pos))
    return zombies

def draw_grid(screen, player, zombies):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if player.position == (x, y):
                pygame.draw.circle(screen, GREEN, rect.center, TILE_SIZE // 4)
            elif any(zombie.position == (x, y) for zombie in zombies):
                pygame.draw.circle(screen, RED, rect.center, TILE_SIZE // 4)

def spawn_zombie(zombies):
    pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    zombies.append(Zombie(pos))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    player = Player(name="Survivor")
    zombies = place_zombies(num_zombies=3)
    grid = generate_grid()

    print("Welcome to the Zombie Survival Game!")
    running = True
    tick_count = 0
    target = False
    last_spawn_time = pygame.time.get_ticks()

    while running and player.health > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move('north')
                elif event.key == pygame.K_s:
                    player.move('south')
                elif event.key == pygame.K_d:
                    player.move('east')
                elif event.key == pygame.K_a:
                    player.move('west')
                elif event.key == pygame.K_SPACE:
                    player.heal()
                elif event.key == pygame.K_UP:
                    target = player.attack(zombies, 'north')
                elif event.key == pygame.K_DOWN:
                    target = player.attack(zombies, 'south')
                elif event.key == pygame.K_RIGHT:
                    target = player.attack(zombies, 'east')
                elif event.key == pygame.K_LEFT:
                    target = player.attack(zombies, 'west')
                
                if target:
                    zombies.remove(target)
                    print("Zombie killed!")
                elif player.ammo == 0:
                    print("Out of ammo!")

        # Spawn new zombie every ZOMBIE_SPAWN_INTERVAL milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= ZOMBIE_SPAWN_INTERVAL:
            spawn_zombie(zombies)
            last_spawn_time = current_time

        # Zombies move every ZOMBIE_MOVE_DELAY ticks
        if tick_count % ZOMBIE_MOVE_DELAY == 0:
            for zombie in zombies:
                zombie.move_towards(player.position)

        # Check for zombie encounters
        for zombie in zombies:
            if zombie.position == player.position:
                player.health -= ZOMBIE_DAMAGE
                time.sleep(1)
                print(f"You've been attacked! {player.health} health remaining")

        # Check if player is still alive
        if player.health <= 0:
            print("You have died! Game over!")
            running = False

        # Game status
        if not zombies:
            print("Congratulations! You have killed all the zombies and survived!")
            running = False

        screen.fill(BLACK)
        draw_grid(screen, player, zombies)

        health_text = font.render(f"Health: {player.health}", True, WHITE)
        ammo_text = font.render(f"Ammo: {player.ammo}", True, WHITE)
        screen.blit(health_text, (10, 10))
        screen.blit(ammo_text, (10, 50))

        pygame.display.flip()
        clock.tick(30)
        tick_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
