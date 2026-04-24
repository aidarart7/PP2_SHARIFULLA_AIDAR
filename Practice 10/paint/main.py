import pygame
import sys

pygame.init()

# Window settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen.fill(WHITE)

# Modes
mode = "brush"   # brush, rectangle, circle, eraser
color = BLACK
radius = 5  # brush size

start_pos = None
clock = pygame.time.Clock()

drawing = False

font = pygame.font.SysFont("Arial", 20)


def draw_text():
    info = [
        "TOOLS",
        "B = Brush",
        "R = Rectangle",
        "C = Circle",
        "E = Eraser",
        "",
        "COLORS",
        "1 = Black",
        "2 = Red",
        "3 = Green",
        "4 = Blue",
        "5 = Yellow",
        "",
        f"Mode: {mode}",
        f"Size: {radius}",
    ]

    y = 10
    for line in info:
        pygame.draw.rect(screen, WHITE, (5, y - 2, 250, 28))
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, y))
        y += 30


while True:
    temp_surface = screen.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Tool selection
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rectangle"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"

            # Color selection
            elif event.key == pygame.K_1:
                color = BLACK
            elif event.key == pygame.K_2:
                color = RED
            elif event.key == pygame.K_3:
                color = GREEN
            elif event.key == pygame.K_4:
                color = BLUE
            elif event.key == pygame.K_5:
                color = YELLOW

            # Brush size control
            elif event.key == pygame.K_UP:
                radius = min(radius + 2, 50)
            elif event.key == pygame.K_DOWN:
                radius = max(radius - 2, 1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rectangle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, rect, 3)

            elif mode == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius_circle = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius_circle, 3)

        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)

    # Redraw helper text area
    pygame.draw.rect(screen, WHITE, (0, 0, 320, 420))
    draw_text()

    pygame.display.flip()
    clock.tick(60)
