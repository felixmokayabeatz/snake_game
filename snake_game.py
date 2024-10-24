import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
GAME_SPEED = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)  # For snake head

# Initialize window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Initialize clock
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)), (cur[1] + (y*BLOCK_SIZE)))
        
        if new in self.positions[2:]:
            return False
        
        if (new[0] < 0 or new[0] >= WINDOW_WIDTH or 
            new[1] < 0 or new[1] >= WINDOW_HEIGHT):
            return False
            
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def render(self, surface):
        # Draw body
        for p in self.positions[1:]:
            pygame.draw.rect(surface, self.color, 
                           (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw head as a triangle
        head = self.positions[0]
        direction = self.direction
        
        # Calculate triangle points based on direction
        if direction == UP:
            p1 = (head[0], head[1])
            p2 = (head[0] + BLOCK_SIZE, head[1] + BLOCK_SIZE)
            p3 = (head[0], head[1] + BLOCK_SIZE)
        elif direction == DOWN:
            p1 = (head[0], head[1] + BLOCK_SIZE)
            p2 = (head[0] + BLOCK_SIZE, head[1])
            p3 = (head[0], head[1])
        elif direction == LEFT:
            p1 = (head[0], head[1])
            p2 = (head[0] + BLOCK_SIZE, head[1] + BLOCK_SIZE)
            p3 = (head[0] + BLOCK_SIZE, head[1])
        else:  # RIGHT
            p1 = (head[0] + BLOCK_SIZE, head[1])
            p2 = (head[0], head[1] + BLOCK_SIZE)
            p3 = (head[0], head[1])
        
        # Draw the head triangle
        pygame.draw.polygon(surface, DARK_GREEN, [p1, p2, p3])
        
        # Add eyes
        eye_color = WHITE
        if direction == UP:
            pygame.draw.circle(surface, eye_color, (head[0] + 5, head[1] + 8), 2)
            pygame.draw.circle(surface, eye_color, (head[0] + 15, head[1] + 8), 2)
        elif direction == DOWN:
            pygame.draw.circle(surface, eye_color, (head[0] + 5, head[1] + 12), 2)
            pygame.draw.circle(surface, eye_color, (head[0] + 15, head[1] + 12), 2)
        elif direction == LEFT:
            pygame.draw.circle(surface, eye_color, (head[0] + 8, head[1] + 5), 2)
            pygame.draw.circle(surface, eye_color, (head[0] + 8, head[1] + 15), 2)
        else:  # RIGHT
            pygame.draw.circle(surface, eye_color, (head[0] + 12, head[1] + 5), 2)
            pygame.draw.circle(surface, eye_color, (head[0] + 12, head[1] + 15), 2)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            r = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), r, 1)

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        if not snake.update():
            snake.reset()
            food.randomize_position()
            continue

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        window.fill(BLACK)
        draw_grid(window)
        snake.render(window)
        food.render(window)
        
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        window.blit(score_text, (5, 5))

        pygame.display.update()
        clock.tick(GAME_SPEED)

if __name__ == '__main__':
    main()