import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = GRID_WIDTH // 2
        self.y = GRID_HEIGHT // 2
        self.direction = "RIGHT"
        self.body = [(self.x, self.y)]
        self.length = 1

    def move(self):
        if self.direction == "UP":
            self.y -= 1
        elif self.direction == "DOWN":
            self.y += 1
        elif self.direction == "LEFT":
            self.x -= 1
        elif self.direction == "RIGHT":
            self.x += 1

        # Update body
        self.body.insert(0, (self.x, self.y))
        if len(self.body) > self.length:
            self.body.pop()

    def check_collision(self):
        # Check wall collision
        if self.x < 0 or self.x >= GRID_WIDTH or self.y < 0 or self.y >= GRID_HEIGHT:
            return True
        # Check self collision
        if (self.x, self.y) in self.body[1:]:
            return True
        return False

    def eat(self, food):
        if self.x == food.x and self.y == food.y:
            self.length += 1
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)

# Game setup
def setup():
    global snake, food, score, game_over
    snake = Snake()
    food = Food()
    score = 0
    game_over = False

# Draw game
def draw():
    screen.fill(BLACK)
    # Draw snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw food
    pygame.draw.rect(screen, RED, (food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    # Draw game over
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    pygame.display.flip()

# Update game loop
def update_loop():
    global food, score, game_over
    if not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"

        # Move snake
        snake.move()

        # Check for food
        if snake.eat(food):
            score += 1
            food.respawn()

        # Check collision
        if snake.check_collision():
            game_over = True

    # Handle restart
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            setup()

    draw()

# Main game loop
async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

# Run game
if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())