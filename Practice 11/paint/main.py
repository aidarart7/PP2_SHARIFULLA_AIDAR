import pygame
import sys
import math

pygame.init()

# -------------------- WINDOW --------------------
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen.fill(WHITE)

# -------------------- SETTINGS --------------------
mode = "brush"   # current drawing mode
color = BLACK
radius = 5

start_pos = None
drawing = False

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# -------------------- UI --------------------
def draw_text():
    """Draw tool info on screen"""
    info = [
        "TOOLS",
        "B = Brush",
        "R = Rectangle",
        "C = Circle",
        "E = Eraser",
        "S = Square",
        "T = Right Triangle",
        "Y = Equilateral Triangle",
        "H = Rhombus",
        "",
        "COLORS",
        "1-5 = Change color",
        "",
        "UP/DOWN = Size",
        f"Mode: {mode}",
        f"Size: {radius}",
    ]

    y = 10
    for line in info:
        pygame.draw.rect(screen, WHITE, (5, y - 2, 320, 28))
        text = font.render(line, True, BLACK)
        screen.blit(text, (10, y))
        y += 30


# =========================================================
# ===================== MAIN LOOP ==========================
# =========================================================

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------------------- KEYBOARD --------------------
        if event.type == pygame.KEYDOWN:

            # tool selection
            if event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rectangle"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_s:
                mode = "square"
            elif event.key == pygame.K_t:
                mode = "right_triangle"
            elif event.key == pygame.K_y:
                mode = "equilateral_triangle"
            elif event.key == pygame.K_h:
                mode = "rhombus"

            # color selection
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

            # brush size
            elif event.key == pygame.K_UP:
                radius = min(radius + 2, 50)
            elif event.key == pygame.K_DOWN:
                radius = max(radius - 2, 1)

        # -------------------- MOUSE DOWN --------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

            # instant drawing for brush/eraser
            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)

        # -------------------- MOUSE UP --------------------
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            # -------- RECTANGLE --------
            if mode == "rectangle":
                rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                   abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, color, rect, 3)

            # -------- CIRCLE --------
            elif mode == "circle":
                r = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, r, 3)

            # -------- SQUARE --------
            elif mode == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                rect = pygame.Rect(x1, y1, side, side)
                pygame.draw.rect(screen, color, rect, 3)

            # -------- RIGHT TRIANGLE --------
            elif mode == "right_triangle":
                points = [
                    (x1, y1),
                    (x2, y2),
                    (x1, y2)
                ]
                pygame.draw.polygon(screen, color, points, 3)

            # -------- EQUILATERAL TRIANGLE (FIXED) --------
            elif mode == "equilateral_triangle":
                dx = x2 - x1
                dy = y2 - y1

                side = int((dx**2 + dy**2)**0.5)
                height = int((math.sqrt(3) / 2) * side)

                # determine direction (up or down)
                direction = -1 if dy < 0 else 1

                # base centered horizontally
                x_center = x1

                points = [
                    (x_center - side // 2, y1),
                    (x_center + side // 2, y1),
                    (x_center, y1 + direction * height)
                ]

                pygame.draw.polygon(screen, color, points, 3)

            # -------- RHOMBUS --------
            elif mode == "rhombus":
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2

                points = [
                    (center_x, center_y - dy),
                    (center_x + dx, center_y),
                    (center_x, center_y + dy),
                    (center_x - dx, center_y)
                ]

                pygame.draw.polygon(screen, color, points, 3)

        # -------------------- MOUSE MOVE --------------------
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(screen, color, event.pos, radius)
            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)

    # redraw UI
    pygame.draw.rect(screen, WHITE, (0, 0, 350, 450))
    draw_text()

    pygame.display.flip()
    clock.tick(60)