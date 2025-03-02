import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Score: 0 | Speed: 10")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
BLACK = (30, 30, 30)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50)

def update_title():
    """Updates the game window title with score and speed."""
    pygame.display.set_caption(f"Snake Game - Score: {score} | Speed: {speed}")

def reset_game():
    """Resets the game state."""
    global snake, snake_dir, food, score, speed, running, paused, game_over
    snake = [(100, 100)]
    snake_dir = (CELL_SIZE, 0)
    food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, 
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
    score = 0
    speed = 10  # Initial Speed
    running = True
    paused = False
    game_over = False
    update_title()  # Update window title

reset_game()  # Start the game initially

# Game Loop
clock = pygame.time.Clock()

def draw_grid():
    """Draws a grid background for a better visual effect."""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def wrap_around(position):
    """Wraps the position around the screen to create an infinite space effect."""
    x, y = position
    if x >= WIDTH: x = 0
    elif x < 0: x = WIDTH - CELL_SIZE
    if y >= HEIGHT: y = 0
    elif y < 0: y = HEIGHT - CELL_SIZE
    return (x, y)

while True:
    screen.fill(BLACK)
    draw_grid()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
            elif event.key == pygame.K_SPACE:  # Pause / Resume
                paused = not paused
            elif event.key == pygame.K_r and game_over:  # Restart after losing
                reset_game()
            elif event.key == pygame.K_s:  # Decrease speed
                speed = max(5, speed - 2)
                update_title()
            elif event.key == pygame.K_w:  # Increase speed
                speed += 2
                update_title()

    if not paused and not game_over:
        # Move the snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        new_head = wrap_around(new_head)  # Apply wrap-around logic
        if new_head in snake:  # Check if snake collides with itself
            game_over = True
        else:
            snake.insert(0, new_head)

        # Check for food collision
        if new_head == food:
            food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE, 
                    random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
            score += 1
            #speed += 1  # Increase speed when food is eaten
            update_title()  # Update title bar
        else:
            snake.pop()  # Remove last segment if no food eaten

    # Draw Snake (Rounded segments for smoother visuals)
    for segment in snake:
        pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE), border_radius=5)
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] + 3, segment[1] + 3, CELL_SIZE - 6, CELL_SIZE - 6), border_radius=5)

    # Draw Food
    pygame.draw.circle(screen, RED, (food[0] + CELL_SIZE // 2, food[1] + CELL_SIZE // 2), CELL_SIZE // 2)

    if paused:
        pause_text = big_font.render("Game Paused", True, YELLOW)
        resume_text = font.render("Press SPACE to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH//2 - 100, HEIGHT//2 - 30))
        screen.blit(resume_text, (WIDTH//2 - 110, HEIGHT//2 + 10))
    if game_over:
        game_over_text = big_font.render("Game Over!", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 30))
        screen.blit(restart_text, (WIDTH//2 - 120, HEIGHT//2 + 10))

    pygame.display.flip()
    clock.tick(speed if not paused else 0)  # Stop game loop when paused
