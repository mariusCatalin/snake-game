import pygame
import random
import math
import time
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (147, 0, 211)
GOLD = (255, 215, 0)

# Pre-calculate grid lines as a surface
def create_grid_surface():
    grid_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
    for x in range(0, WINDOW_SIZE, GRID_SIZE):
        pygame.draw.line(grid_surface, (20, 20, 20), (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, GRID_SIZE):
        pygame.draw.line(grid_surface, (20, 20, 20), (0, y), (WINDOW_SIZE, y))
    return grid_surface

class ParticleEffect:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        self.particles = []
        self.x = x
        self.y = y
        self.color = color
        self.create_particles()
        
    def create_particles(self):
        # Reduced number of particles for better performance
        for _ in range(10):  # Changed from 20 to 10
            particle = {
                'x': self.x,
                'y': self.y,
                'velocity': [random.uniform(-4, 4), random.uniform(-4, 4)],
                'lifetime': 20,  # Reduced lifetime
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['velocity'][0]
            particle['y'] += particle['velocity'][1]
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            alpha = int((particle['lifetime'] / 20) * 255)  # Updated from 30 to 20
            particle_color = (*self.color, alpha)
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, 
                             (particle['size']//2, particle['size']//2), 
                             particle['size']//2)
            screen.blit(particle_surface, (particle['x'], particle['y']))

class PowerUp:
    def __init__(self, x: int, y: int, power_type: str):
        self.x = x
        self.y = y
        self.type = power_type
        self.animation_offset = 0
        self.active = True
    
    def draw(self, screen):
        if not self.active:
            return
            
        self.animation_offset = (self.animation_offset + 0.1) % (2 * math.pi)
        offset = math.sin(self.animation_offset) * 5
        
        if self.type == 'speed':
            color = BLUE
        elif self.type == 'invincibility':
            color = PURPLE
        else:  # points
            color = GOLD
            
        pygame.draw.rect(screen, color, 
                        (self.x * GRID_SIZE, 
                         self.y * GRID_SIZE + offset, 
                         GRID_SIZE, GRID_SIZE))

# Pre-calculated rainbow colors for better performance
RAINBOW_COLORS = []
for i in range(360):
    hue = i
    c = 1
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = 0
    
    if 0 <= hue < 60:
        r, g, b = c, x, 0
    elif 60 <= hue < 120:
        r, g, b = x, c, 0
    elif 120 <= hue < 180:
        r, g, b = 0, c, x
    elif 180 <= hue < 240:
        r, g, b = 0, x, c
    elif 240 <= hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
        
    RAINBOW_COLORS.append((int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)))

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 1
        self.positions = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.growing = False
        self.speed_boost = 1.0
        self.invincible = False
        self.effects = []
        self.rainbow_mode = False
        self.rainbow_index = 0
        self.move_timer = 0
        self.move_delay = 150  # milliseconds between moves
    
    def get_head_position(self) -> Tuple[int, int]:
        return self.positions[0]
    
    def update_rainbow(self):
        if self.rainbow_mode:
            self.rainbow_index = (self.rainbow_index + 5) % 360
    
    def get_rainbow_color(self, segment_index: int) -> Tuple[int, int, int]:
        # Use pre-calculated colors
        index = (self.rainbow_index + segment_index * 20) % 360
        return RAINBOW_COLORS[index]
    
    def turn(self, point: Tuple[int, int]):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def should_move(self, current_time):
        delay = self.move_delay / self.speed_boost
        if current_time - self.move_timer >= delay:
            self.move_timer = current_time
            return True
        return False
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x, cur[1] + y)
        
        if new[0] < 0:
            new = (GRID_COUNT - 1, new[1])
        elif new[0] >= GRID_COUNT:
            new = (0, new[1])
            
        if new[1] < 0:
            new = (new[0], GRID_COUNT - 1)
        elif new[1] >= GRID_COUNT:
            new = (new[0], 0)
            
        if not self.invincible and new in self.positions[2:]:
            return False
            
        self.positions.insert(0, new)
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False
        return True
    
    def draw(self, screen):
        self.update_rainbow()
        for i, p in enumerate(self.positions):
            if self.rainbow_mode:
                color = self.get_rainbow_color(i)
            else:
                color = GREEN
            
            rect = pygame.Rect(p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 100, 0), rect, 1)
        
        # Draw eyes on the head
        head = self.positions[0]
        eye_color = WHITE if not self.invincible else PURPLE
        eye_size = GRID_SIZE // 4
        
        # Adjust eye positions based on direction
        if self.direction == (1, 0):  # Right
            eye_positions = [(0.7, 0.25), (0.7, 0.75)]
        elif self.direction == (-1, 0):  # Left
            eye_positions = [(0.3, 0.25), (0.3, 0.75)]
        elif self.direction == (0, -1):  # Up
            eye_positions = [(0.25, 0.3), (0.75, 0.3)]
        else:  # Down
            eye_positions = [(0.25, 0.7), (0.75, 0.7)]
            
        for ex, ey in eye_positions:
            pygame.draw.circle(screen, eye_color,
                             (int(head[0] * GRID_SIZE + ex * GRID_SIZE),
                              int(head[1] * GRID_SIZE + ey * GRID_SIZE)),
                             eye_size)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Neon Snake")
        self.clock = pygame.time.Clock()
        self.grid_surface = create_grid_surface()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.reset()
        
    def reset(self):
        self.snake = Snake()
        self.food = self.place_food()
        self.power_ups = []
        self.effects = []
        self.power_up_timer = 0
        self.game_over = False
        self.power_up_duration = 200  # frames for power-up effect
        self.speed_timer = 0
        self.invincibility_timer = 0
        self.rainbow_timer = 0
        
    def place_food(self) -> Tuple[int, int]:
        while True:
            position = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            if position not in self.snake.positions:
                return position
                
    def spawn_power_up(self):
        if len(self.power_ups) >= 2:
            return
            
        position = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
        if position not in self.snake.positions and position != self.food:
            power_type = random.choice(['speed', 'invincibility', 'points'])
            self.power_ups.append(PowerUp(position[0], position[1], power_type))
    
    def handle_power_up_collision(self, power_up: PowerUp):
        if power_up.type == 'speed':
            self.snake.speed_boost = 2.0
            self.speed_timer = self.power_up_duration
            self.effects.append(ParticleEffect(
                power_up.x * GRID_SIZE, power_up.y * GRID_SIZE, BLUE))
        elif power_up.type == 'invincibility':
            self.snake.invincible = True
            self.invincibility_timer = self.power_up_duration
            self.effects.append(ParticleEffect(
                power_up.x * GRID_SIZE, power_up.y * GRID_SIZE, PURPLE))
        else:  # points
            self.snake.score += 50
            self.snake.rainbow_mode = True
            self.rainbow_timer = self.power_up_duration
            self.effects.append(ParticleEffect(
                power_up.x * GRID_SIZE, power_up.y * GRID_SIZE, GOLD))
        
        power_up.active = False
        self.power_ups.remove(power_up)
    
    def update_power_ups(self):
        # Update power-up timers and reset effects when they expire
        if self.speed_timer > 0:
            self.speed_timer -= 1
            if self.speed_timer == 0:
                self.snake.speed_boost = 1.0
                
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1
            if self.invincibility_timer == 0:
                self.snake.invincible = False
                
        if self.rainbow_timer > 0:
            self.rainbow_timer -= 1
            if self.rainbow_timer == 0:
                self.snake.rainbow_mode = False
    
    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                        continue
                        
                    if event.key == pygame.K_UP:
                        self.snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn((1, 0))
            
            if self.game_over:
                self.draw()
                self.clock.tick(FPS)
                continue
            
            # Update power-up status
            self.update_power_ups()
            
            # Move snake with timing-based movement instead of frame-based
            if self.snake.should_move(current_time):
                if not self.snake.move():
                    self.game_over = True
            
            # Check for food collision
            if self.snake.get_head_position() == self.food:
                self.snake.growing = True
                self.snake.length += 1
                self.snake.score += 10
                self.food = self.place_food()
                self.effects.append(ParticleEffect(
                    self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, RED))
            
            # Power-up spawning and collision detection
            self.power_up_timer += 1
            if self.power_up_timer >= 100:
                self.spawn_power_up()
                self.power_up_timer = 0
            
            for power_up in self.power_ups[:]:
                if self.snake.get_head_position() == (power_up.x, power_up.y):
                    self.handle_power_up_collision(power_up)
            
            # Update effects
            for effect in self.effects[:]:
                effect.update()
                if not effect.particles:
                    self.effects.remove(effect)
            
            self.draw()
            self.clock.tick(FPS)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid lines using pre-computed surface
        self.screen.blit(self.grid_surface, (0, 0))
        
        # Draw food with pulsing effect
        food_rect = pygame.Rect(
            self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 255  # Reduced frequency
        food_color = (255, int(pulse), int(pulse))
        pygame.draw.rect(self.screen, food_color, food_rect)
        
        # Draw power-ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw snake
        self.snake.draw(self.screen)
        
        # Draw effects
        for effect in self.effects:
            effect.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.snake.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw power-up indicators
        if self.speed_timer > 0:
            speed_text = self.font.render("SPEED", True, BLUE)
            self.screen.blit(speed_text, (WINDOW_SIZE - 100, 10))
            
        if self.invincibility_timer > 0:
            invincible_text = self.font.render("INVINCIBLE", True, PURPLE)
            self.screen.blit(invincible_text, (WINDOW_SIZE - 150, 50))
            
        if self.rainbow_timer > 0:
            rainbow_text = self.font.render("RAINBOW", True, GOLD)
            self.screen.blit(rainbow_text, (WINDOW_SIZE - 120, 90))
        
        if self.game_over:
            game_over_text = self.big_font.render('Game Over!', True, RED)
            restart_text = self.big_font.render('Press R to Restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            restart_rect = restart_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 50))
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run() 