import pygame
import sys
from datetime import datetime

# import from tools.py
from tools import flood_fill, draw_shape

pygame.init()

# -------------------- WINDOW --------------------
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# -------------------- COLORS --------------------
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

color = BLACK

# -------------------- MODES --------------------
mode = "pencil"
drawing = False
start_pos = None
last_pos = None

# -------------------- BRUSH --------------------
brush_sizes = [2, 5, 10]
brush_index = 1
radius = brush_sizes[brush_index]

# -------------------- TEXT --------------------
font = pygame.font.SysFont("Arial", 24)
text_input = ""
typing = False
text_pos = None

clock = pygame.time.Clock()

# =========================================================
# ===================== FUNCTIONS ==========================
# =========================================================

def save_canvas():
    """Save canvas with timestamp"""
    filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)

# =========================================================
# ===================== MAIN LOOP ==========================
# =========================================================

while True:

    temp = canvas.copy()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ---------------- KEYBOARD ----------------
        if event.type == pygame.KEYDOWN:

            if typing:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_input, True, color)
                    canvas.blit(text_surface, text_pos)
                    typing = False
                    text_input = ""

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

            else:
                # tools
                if event.key == pygame.K_p:
                    mode = "pencil"
                elif event.key == pygame.K_l:
                    mode = "line"
                elif event.key == pygame.K_r:
                    mode = "rect"
                elif event.key == pygame.K_c:
                    mode = "circle"
                elif event.key == pygame.K_f:
                    mode = "fill"
                elif event.key == pygame.K_t:
                    mode = "text"
                elif event.key == pygame.K_s:
                    mode = "square"
                elif event.key == pygame.K_y:
                    mode = "equilateral"
                elif event.key == pygame.K_h:
                    mode = "rhombus"
                elif event.key == pygame.K_g:
                    mode = "right_triangle"

                # colors
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

                # brush sizes
                elif event.key == pygame.K_6:
                    brush_index = 0
                elif event.key == pygame.K_7:
                    brush_index = 1
                elif event.key == pygame.K_8:
                    brush_index = 2

                radius = brush_sizes[brush_index]

                # save
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

        # ---------------- MOUSE ----------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = event.pos
            last_pos = event.pos
            drawing = True

            if mode == "fill":
                flood_fill(canvas, *event.pos, color)

            elif mode == "text":
                typing = True
                text_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

            if mode in ["line","rect","circle","square","right_triangle","equilateral","rhombus"]:
                draw_shape(canvas, mode, start_pos, event.pos, color, radius)

        elif event.type == pygame.MOUSEMOTION and drawing:
            if mode == "pencil":
                pygame.draw.line(canvas, color, last_pos, event.pos, radius)
                last_pos = event.pos

    # ---------------- DRAW ----------------
    screen.blit(canvas, (0,0))

    # preview line
    if drawing and mode == "line":
        pygame.draw.line(screen, color, start_pos, pygame.mouse.get_pos(), radius)

    # preview shapes
    if drawing and mode in ["rect","circle","square","right_triangle","equilateral","rhombus"]:
        draw_shape(screen, mode, start_pos, pygame.mouse.get_pos(), color, radius)

    # text preview
    if typing:
        text_surface = font.render(text_input, True, color)
        screen.blit(text_surface, text_pos)

    pygame.display.flip()
    clock.tick(60)