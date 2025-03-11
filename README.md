# Neon Snake Game

A modern take on the classic Snake game with stunning visual effects, power-ups, and unique gameplay mechanics built with Python and Pygame.

![Neon Snake Game](screenshots/gameplay.png) <!-- Add your screenshot here -->

## Features

- **Modern Visual Effects**:
  - Particle explosions when collecting food and power-ups
  - Pulsing food with dynamic color changes
  - Snake eyes that follow the direction of movement
  - Subtle grid background
  - Smooth animations for power-ups

- **Innovative Power-up System**:
  - **Speed Boost** (Blue): Temporarily increases snake movement speed
  - **Invincibility** (Purple): Allows passing through your own body
  - **Rainbow Mode** (Gold): Gives bonus points and makes your snake cycle through rainbow colors

- **Advanced Game Mechanics**:
  - Wrap-around screen edges
  - Anti-reverse protection
  - Performance-optimized rendering
  - Time-based movement system for consistent gameplay

## Installation

### Prerequisites
- Python 3.6 or newer
- Pip (Python package installer)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/neon-snake.git
cd neon-snake
```

2. Create a virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Run the game:
```bash
python snake_game.py
```

## How to Play

- Use **arrow keys** to change direction
- Collect **red food** to grow and increase your score
- Pick up special **power-ups** for temporary abilities:
  - **Blue**: Speed boost
  - **Purple**: Invincibility (pass through yourself)
  - **Gold**: Points bonus + rainbow mode
- Press **R** to restart when game over
- Close the window to quit

## Performance Tips

If the game runs slowly on your system:
- Close other applications that might be using system resources
- Lower the resolution by changing `WINDOW_SIZE` and `GRID_SIZE` constants
- Disable some visual effects by modifying the code

## Technical Implementation

The game uses several optimization techniques:
- Pre-rendered surfaces for static elements
- Pre-calculated color tables
- Time-based movement instead of frame-based
- Optimized particle system
- Object pooling for game entities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Game developed by [Your Name]
- Built with [Pygame](https://www.pygame.org/)
- Inspired by the classic Snake game

## Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## Future Improvements

- High score system with persistent storage
- Multiple levels with increasing difficulty
- Additional power-ups and obstacles
- Sound effects and background music
- Game settings menu

---

*Note: This README template is designed for GitHub. Make sure to add real screenshots of your game and update the GitHub username in the installation instructions.* 