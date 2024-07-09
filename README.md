 # Zombie Survival Game

Welcome to the Zombie Survival Game! This game is a simple yet engaging Pygame project where you, as the player, must survive a zombie apocalypse by navigating a grid, attacking zombies, and healing yourself.

## Game Overview

- **Grid Size:** 15x15 tiles
- **Tile Size:** 100x100 pixels
- **Player Starting Health:** 100
- **Player Starting Ammo:** 5
- **Zombie Damage:** 15 per attack
- **Health Pack Heal:** 20 per pack
- **Zombie Move Delay:** Every 50 ticks
- **Zombie Spawn Interval:** Every 5 seconds

## Game Features

- **Player Movement:** Move the player around the grid using WASD keys.
- **Attack Zombies:** Attack zombies using the arrow keys.
- **Heal:** Heal yourself using the space bar, provided you have health packs.
- **Zombies:** Zombies move towards the player and attack when they reach the player's position.
- **Item Effects:** Health packs can be used to heal, and power-ups can eliminate nearby zombies.

## Controls

- **W:** Move North
- **A:** Move West
- **S:** Move South
- **D:** Move East
- **UP Arrow:** Attack North
- **DOWN Arrow:** Attack South
- **LEFT Arrow:** Attack West
- **RIGHT Arrow:** Attack East
- **Space Bar:** Heal (requires a health pack)

## How to Play

1. **Clone the Repository:**
   ```
   git clone https://github.com/yourusername/zombie-survival-game.git
   cd zombie-survival-game
   ```

2. **Install Pygame:**
Ensure you have Pygame installed. You can install it using pip:

  ```sh
  pip install pygame
  ```

3. **Run the Game:**

  ```sh
  python game.py
  ```
4. **Gameplay:**

Navigate through the grid using WASD keys.
Attack zombies when they are adjacent to you using the arrow keys.
Heal yourself with the space bar when needed and if you have health packs.
Survive as long as you can while zombies continuously spawn every 5 seconds.

# Game Development

This project was developed as part of learning Pygame and game development. It includes fundamental game mechanics such as movement, attacks, healing, and enemy AI behavior. Feel free to fork the project and make your own enhancements!

# Contributions

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

# License

This project is licensed under the MIT License.
