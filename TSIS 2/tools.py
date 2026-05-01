import pygame
import math

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= surface.get_width():
            continue
        if py < 0 or py >= surface.get_height():
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.extend([
            (px+1, py), (px-1, py),
            (px, py+1), (px, py-1)
        ])


def draw_shape(surface, mode, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    if mode == "rect":
        rect = pygame.Rect(min(x1,x2), min(y1,y2),
                           abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, rect, width)

    elif mode == "circle":
        r = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
        pygame.draw.circle(surface, color, start, r, width)

    elif mode == "square":
        side = min(abs(x2-x1), abs(y2-y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(surface, color, rect, width)

    elif mode == "right_triangle":
        pts = [(x1,y1),(x2,y2),(x1,y2)]
        pygame.draw.polygon(surface, color, pts, width)

    elif mode == "equilateral":
        dx = x2-x1
        dy = y2-y1
        side = int((dx**2 + dy**2)**0.5)
        h = int((math.sqrt(3)/2)*side)
        direction = -1 if dy < 0 else 1

        pts = [
            (x1 - side//2, y1),
            (x1 + side//2, y1),
            (x1, y1 + direction*h)
        ]
        pygame.draw.polygon(surface, color, pts, width)

    elif mode == "rhombus":
        cx = (x1+x2)//2
        cy = (y1+y2)//2
        dx = abs(x2-x1)//2
        dy = abs(y2-y1)//2

        pts = [
            (cx,cy-dy),
            (cx+dx,cy),
            (cx,cy+dy),
            (cx-dx,cy)
        ]
        pygame.draw.polygon(surface, color, pts, width)