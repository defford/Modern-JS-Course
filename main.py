import pygame
import random
import time
from player import Player
from enemy import Zombie, place_zombies
from item import Item, spawn_item

# Constants
GRID_SIZE = 15
TILE_SIZE = 40
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
ZOMBIE_DAMAGE = 15
ZOMBIE_MOVE_DELAY = 50  # Zombies move every second tick
ZOMBIE_SPAWN_INTERVAL = 4000  # Spawn a zombie every 4 seconds
ITEM_SPAWN_INTERVAL = 7000  # Spawn an item every 7 seconds
ATTACK_INTERVAL = 2000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def generate_grid():
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return grid

def draw_grid(screen, player, zombies, items):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if player.position == (x, y):
                pygame.draw.circle(screen, GREEN, rect.center, TILE_SIZE // 4)
            elif any(zombie.position == (x, y) for zombie in zombies):
                pygame.draw.circle(screen, RED, rect.center, TILE_SIZE // 4)
            elif any(item.position == (x, y) for item in items):
                pygame.draw.circle(screen, BLUE, rect.center, TILE_SIZE // 4)

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
    items = []
    grid = generate_grid()

    print("Welcome to the Zombie Survival Game!")
    running = True
    tick_count = 0
    last_zombie_spawn_time = pygame.time.get_ticks()
    last_item_spawn_time = pygame.time.get_ticks()
    last_attack_time = pygame.time.get_ticks()

    while running and player.health > 0:
        target = None  # Initialize target at the start of each loop iteration
        
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
                
                if target is not None and target in zombies:
                    zombies.remove(target)
                    print("Zombie killed!")
                elif player.ammo == 0:
                    print("Out of ammo!")

        # Spawn new zombie every ZOMBIE_SPAWN_INTERVAL milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - last_zombie_spawn_time >= ZOMBIE_SPAWN_INTERVAL:
            spawn_zombie(zombies)
            last_zombie_spawn_time = current_time

        # Spawn new item every ITEM_SPAWN_INTERVAL milliseconds
        if current_time - last_item_spawn_time >= ITEM_SPAWN_INTERVAL:
            items.append(spawn_item())
            last_item_spawn_time = current_time

        # Zombies move every ZOMBIE_MOVE_DELAY ticks
        if tick_count % ZOMBIE_MOVE_DELAY == 0:
            for zombie in zombies:
                zombie.move_towards(player.position)

        # Check for zombie encounters
        for zombie in zombies:
            if current_time - last_attack_time >= ATTACK_INTERVAL:
                canAttack = True
            if zombie.position == player.position and canAttack == True:
                player.health -= ZOMBIE_DAMAGE
                canAttack = False
                last_attack_time = current_time
                print(f"You've been attacked! {player.health} health remaining")

        # Check if player is still alive
        if player.health <= 0:
            print("You have died! Game over!")
            running = False

        # Check for item encounters
        for item in items:
            if item.position == player.position:
                item.apply_effect(player, zombies)
                items.remove(item)
                print(f"Picked up a {item.item_type}!")

        # Game status
        if not zombies:
            print("Congratulations! You have killed all the zombies and survived!")
            running = False

        screen.fill(BLACK)
        draw_grid(screen, player, zombies, items)

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
